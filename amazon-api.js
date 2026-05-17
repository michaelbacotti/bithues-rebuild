/**
 * amazon-api.js — Amazon Creators API client for Bithues
 * Supports both v2.x (Cognito) and v3.x (LWA) credential formats
 *
 * Auth flow: OAuth2 client_credentials → Bearer token
 * Token cached in sessionStorage (60-min TTL)
 *
 * Credentials are read from window.AMAZON_CONFIG at runtime:
 *   { credentialId, credentialSecret, version, partnerTag }
 * On Cloudflare Pages: inject via env vars (AMAZON_CREDENTIAL_ID etc.)
 * in a _routes.json rewrite or Worker — NEVER commit credentials.
 *
 * Fallback: If API auth fails (AssociateNotEligible / 401 / network error),
 * all functions return empty arrays gracefully so the UI stays functional.
 */

(function (root) {
  'use strict';

  // ── Config ────────────────────────────────────────────────────────────────
  //
  // Credentials are read from window.AMAZON_CONFIG if set (env-injected).
  // Otherwise uses hardcoded placeholders — which will not work.
  // On Cloudflare Pages: set env vars AMAZON_CREDENTIAL_ID / AMAZON_CREDENTIAL_SECRET / AMAZON_VERSION
  // and use a _routes.json rewrite or Worker to inject them into this file at deploy time.
  //
  var _cfg = (typeof window !== 'undefined' && window.AMAZON_CONFIG) || {};
  var CONFIG = {
    amazonCredentialKey:     _cfg.credentialId     || null,
    amazonCredentialVal: _cfg.credentialSecret || null,
    version:          _cfg.version          || '3.1',

    // OAuth2 token endpoints by version
    tokenEndpoints: {
      '2.1': 'https://creatorsapi.auth.us-east-1.amazoncognito.com/oauth2/token',
      '2.2': 'https://creatorsapi.auth.eu-south-2.amazoncognito.com/oauth2/token',
      '2.3': 'https://creatorsapi.auth.us-west-2.amazoncognito.com/oauth2/token',
      '3.1': 'https://api.amazon.com/auth/o2/token',          // US
      '3.2': 'https://api.amazon.co.uk/auth/o2/token',         // UK
      '3.3': 'https://api.amazon.co.jp/auth/o2/token',         // JP
    },

    // Creators API base + catalog endpoint
    baseUrl:    'https://creatorsapi.amazon.com',
    searchPath: '/catalog/v1/searchItems',
    getPath:    '/catalog/v1/getItems',

    // Marketplace
    marketplace: 'www.amazon.com',

    // Partner tag (associate tag)
    partnerTag: 'michaelbacoti-20',

    // Token TTL in ms (Amazon tokens expire after ~3600s, use 3300s to be safe)
    tokenTTL: 3300 * 1000,

    // Cache key
    tokenCacheKey: 'amazonCreatorsToken',
    tokenExpiryKey: 'amazonCreatorsTokenExpiry',
  };

  // ── Token Cache ───────────────────────────────────────────────────────────
  function getCachedToken() {
    try {
      var token  = sessionStorage.getItem(CONFIG.tokenCacheKey);
      var expiry = parseInt(sessionStorage.getItem(CONFIG.tokenExpiryKey) || '0', 10);
      if (token && Date.now() < expiry) {
        return token;
      }
    } catch (e) { /* sessionStorage not available */ }
    return null;
  }

  function setCachedToken(token) {
    try {
      sessionStorage.setItem(CONFIG.tokenCacheKey, token);
      sessionStorage.setItem(CONFIG.tokenExpiryKey, String(Date.now() + CONFIG.tokenTTL));
    } catch (e) { /* ignore */ }
  }

  function clearCachedToken() {
    try {
      sessionStorage.removeItem(CONFIG.tokenCacheKey);
      sessionStorage.removeItem(CONFIG.tokenExpiryKey);
    } catch (e) { /* ignore */ }
  }

  // ── OAuth2 Token Acquisition ────────────────────────────────────────────────
  /**
   * Acquire OAuth2 access token using client_credentials grant.
   * @returns {Promise<string>} Bearer token
   */
  function acquireToken() {
    return new Promise(function (resolve, reject) {
      // Check cache first
      var cached = getCachedToken();
      if (cached) { resolve(cached); return; }

      var ep = CONFIG.tokenEndpoints[CONFIG.version];
      if (!ep) {
        reject(new Error('Unknown credential version: ' + CONFIG.version));
        return;
      }

      var credentials = CONFIG.amazonCredentialKey + ':' + CONFIG.amazonCredentialVal;
      var authHeader  = 'Basic ' + btoa(credentials);

      var scope = CONFIG.version.startsWith('3.')
        ? 'creatorsapi::default'
        : 'creatorsapi/default';

      var body = [
        'grant_type=client_credentials',
        'client_id='    + encodeURIComponent(CONFIG.amazonCredentialKey),
        'client_secret=' + encodeURIComponent(CONFIG.amazonCredentialVal),
        'scope='        + encodeURIComponent(scope),
      ].join('&');

      var xhr = new XMLHttpRequest();
      xhr.open('POST', ep, true);
      xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
      xhr.setRequestHeader('Authorization', authHeader);
      xhr.timeout = 15000;

      xhr.onload = function () {
        if (xhr.status >= 200 && xhr.status < 300) {
          try {
            var data = JSON.parse(xhr.responseText);
            var token = data.access_token;
            if (!token) {
              reject(new Error('No access_token in OAuth response'));
              return;
            }
            setCachedToken(token);
            resolve(token);
          } catch (e) {
            reject(new Error('Failed to parse OAuth response: ' + e.message));
          }
        } else {
          // Log error body for debugging; don't surface to UI
          var errMsg = 'OAuth2 token request failed: HTTP ' + xhr.status;
          try { errMsg += ' — ' + xhr.responseText; } catch (e) {}
          console.warn('[amazon-api] ' + errMsg);
          reject(new Error(errMsg));
        }
      };

      xhr.onerror = function () {
        reject(new Error('Network error acquiring OAuth token'));
      };

      xhr.ontimeout = function () {
        reject(new Error('OAuth token request timed out'));
      };

      xhr.send(body);
    });
  }

  // ── API Request Helper ─────────────────────────────────────────────────────
  /**
   * Make an authenticated Creators API request.
   * @param {string} method   - 'GET' or 'POST'
   * @param {string} path    - API path (e.g. '/catalog/v1/searchItems')
   * @param {object} body    - Request body (will be JSON-serialized)
   * @returns {Promise<object>} Parsed JSON response
   */
  function apiRequest(method, path, body) {
    return acquireToken().then(function (token) {
      return new Promise(function (resolve, reject) {
        var url = CONFIG.baseUrl + path;
        var xhr = new XMLHttpRequest();

        if (method === 'GET') {
          xhr.open(method, url, true);
        } else {
          xhr.open(method, url, true);
          xhr.setRequestHeader('Content-Type', 'application/json');
        }
        xhr.setRequestHeader('Authorization', 'Bearer ' + token);
        xhr.setRequestHeader('x-amz-marketplace', CONFIG.marketplace);
        xhr.timeout = 20000;

        xhr.onload = function () {
          if (xhr.status >= 200 && xhr.status < 300) {
            try {
              resolve(JSON.parse(xhr.responseText));
            } catch (e) {
              reject(new Error('Failed to parse API response: ' + e.message));
            }
          } else {
            // Handle auth failures — clear token cache so next attempt retries auth
            if (xhr.status === 401 || xhr.status === 403) {
              clearCachedToken();
            }
            var errMsg = 'Creators API ' + method + ' ' + path + ' failed: HTTP ' + xhr.status;
            try { errMsg += ' — ' + xhr.responseText; } catch (e) {}
            console.warn('[amazon-api] ' + errMsg);
            reject(new Error(errMsg));
          }
        };

        xhr.onerror = function () {
          reject(new Error('Network error calling Creators API'));
        };

        xhr.ontimeout = function () {
          reject(new Error('Creators API request timed out'));
        };

        if (body) {
          xhr.send(JSON.stringify(body));
        } else {
          xhr.send();
        }
      });
    });
  }

  // ── Search ────────────────────────────────────────────────────────────────
  /**
   * Search Amazon product catalog.
   * @param {string} keyword  - Search keyword(s)
   * @param {number} [count]  - Max results (default 4)
   * @returns {Promise<Array>} Array of product objects: { asin, title, price, image, link }
   */
  function searchProducts(keyword, count) {
    count = count || 4;

    var resources = [
      'images.primary.medium',
      'itemInfo.title',
      'itemInfo.byLineInfo',
      'offersV2.listings.price',
      'offersV2.listings.availability',
    ].map(function (r) { return r; });

    var body = {
      keywords:     keyword,
      partnerTag:   CONFIG.partnerTag,
      resources:   resources,
      itemCount:   count,
    };

    return apiRequest('POST', CONFIG.searchPath, body).then(function (response) {
      var items = response.items || [];
      return items.map(function (item) {
        var asin     = item.asin || '';
        var title    = getNested(item, 'itemInfo.title.displayString', '');
        var byLine   = getNested(item, 'itemInfo.byLineInfo.name', '');
        var imageUrl = getNested(item, 'images.primary.medium.url', '');
        var priceAmt = getNested(item, 'offersV2.listings.price.amount', '');
        var priceSym = getNested(item, 'offersV2.listings.price.currencySymbol', '$');
        var avail    = getNested(item, 'offersV2.listings.availability.status', 'UNKNOWN');

        var price = priceAmt ? priceSym + priceAmt : null;

        return {
          asin:    asin,
          title:   title,
          author:  byLine || '',
          price:   price,
          image:   imageUrl,
          link:    makeAffiliateUrl(asin),
          available: avail === 'AVAILABLE' || avail === 'INCLUDEABLE',
        };
      });
    }).catch(function (err) {
      console.warn('[amazon-api] searchProducts failed, returning empty: ' + err.message);
      return [];
    });
  }

  // ── Get Single Product ─────────────────────────────────────────────────────
  /**
   * Get details for a single ASIN.
   * @param {string} asin
   * @returns {Promise<object|null>} Product object or null if not found
   */
  function getProduct(asin) {
    var resources = [
      'images.primary.medium',
      'itemInfo.title',
      'itemInfo.byLineInfo',
      'itemInfo.features',
      'offersV2.listings.price',
      'offersV2.listings.availability',
      'offersV2.listings.condition',
    ];

    var body = {
      partnerTag: CONFIG.partnerTag,
      itemIds:   [asin],
      resources: resources,
    };

    return apiRequest('POST', CONFIG.getPath, body).then(function (response) {
      var items = response.items || [];
      if (!items.length) { return null; }

      var item = items[0];
      var asin     = item.asin || '';
      var title    = getNested(item, 'itemInfo.title.displayString', '');
      var byLine   = getNested(item, 'itemInfo.byLineInfo.name', '');
      var features = getNested(item, 'itemInfo.features.featureList', []).map(function (f) { return f; });
      var imageUrl = getNested(item, 'images.primary.medium.url', '');
      var priceAmt = getNested(item, 'offersV2.listings.price.amount', '');
      var priceSym = getNested(item, 'offersV2.listings.price.currencySymbol', '$');
      var avail    = getNested(item, 'offersV2.listings.availability.status', 'UNKNOWN');
      var cond     = getNested(item, 'offersV2.listings.condition', 'NEW');

      var price = priceAmt ? priceSym + priceAmt : null;

      return {
        asin:     asin,
        title:    title,
        author:   byLine || '',
        features: features,
        price:    price,
        image:    imageUrl,
        link:     makeAffiliateUrl(asin),
        available: avail === 'AVAILABLE' || avail === 'INCLUDEABLE',
        condition: cond,
      };
    }).catch(function (err) {
      console.warn('[amazon-api] getProduct(' + asin + ') failed: ' + err.message);
      return null;
    });
  }

  // ── Affiliate URL ─────────────────────────────────────────────────────────
  /**
   * Build an Amazon affiliate link for a given ASIN.
   * @param {string} asin
   * @returns {string}
   */
  function makeAffiliateUrl(asin) {
    return 'https://www.amazon.com/dp/' + asin + '?tag=' + CONFIG.partnerTag;
  }

  // ── Utility: safe nested property access ──────────────────────────────────
  /**
   * Get a nested property from an object using dot-notation path.
   * e.g. getNested(item, 'offersV2.listings.price.amount', '')
   */
  function getNested(obj, path, defaultVal) {
    var parts = path.split('.');
    var val   = obj;
    for (var i = 0; i < parts.length; i++) {
      if (val === null || val === undefined) { return defaultVal; }
      val = val[parts[i]];
    }
    return (val === null || val === undefined) ? defaultVal : val;
  }

  // ── Public API ────────────────────────────────────────────────────────────
  //
  // NOTE: The Creators API requires 10+ qualifying sales in trailing 30 days.
  // If the API returns AssociateNotEligible / 401 / network errors, all
  // functions fall back to empty arrays so the UI stays functional.
  // Related-books fallback data is embedded directly in the page scripts
  // (see review page modifications) using real ASINs from book-tracker.md.
  //
  root.AmazonAPI = {
    searchProducts:  searchProducts,
    getProduct:       getProduct,
    makeAffiliateUrl: makeAffiliateUrl,
    // Expose config for debugging / per-page overrides
    config: CONFIG,
  };

})(window);