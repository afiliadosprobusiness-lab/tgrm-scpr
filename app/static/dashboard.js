(() => {
  const i18n = {
    es: {
      pageTitle: "Panel Multi-Fuente",
      navTitle: "Scraper Multi-Fuente",
      menuLabel: "Plataformas",
      navTelegram: "Telegram",
      navGoogleMaps: "Google Maps",
      navOpenStreetMap: "OpenStreetMap",
      navReddit: "Reddit",
      navFoursquare: "Foursquare",
      navYelp: "Yelp",
      navTomTom: "TomTom",
      navOpenCorporates: "OpenCorporates",
      heroTitle: "Control y Descubrimiento",
      heroLede: "Elige una fuente, define filtros y ejecuta recoleccion de datos de forma segura.",
      languageLabel: "Idioma",
      themeLabel: "Color",
      langSpanish: "Espanol",
      langEnglish: "English",
      themeLight: "Claro",
      themeDark: "Oscuro",
      metricTargetsDb: "Targets en DB",
      metricMessagesStored: "Mensajes guardados",
      metricConfigTargets: "Targets configurados",
      sourceSearchTitle: "Busqueda y Filtros por Fuente",
      sourceQueryLabel: "Busqueda",
      sourceQueryPlaceholder: "Ej: restaurantes vegan en Lima",
      sourceNicheLabel: "Nicho de negocio",
      nicheAll: "Todos los nichos",
      nicheRestaurants: "Restaurantes",
      nicheRealEstate: "Inmobiliaria",
      nicheLegal: "Servicios legales",
      nicheMedical: "Clinicas medicas",
      nicheBeauty: "Belleza y bienestar",
      sourceWebsiteLabel: "Tiene web",
      sourcePhoneLabel: "Tiene telefono",
      filterAny: "Cualquiera",
      filterYes: "Si",
      filterNo: "No",
      sourceLocationLabel: "Ubicacion",
      sourceLocationPlaceholder: "Ciudad o pais",
      sourceRatingLabel: "Rating minimo",
      ratingAny: "Cualquiera",
      sourceVerifiedLabel: "Solo perfiles verificados",
      applyFiltersBtn: "Aplicar filtros",
      resetFiltersBtn: "Reiniciar",
      credentialInputLabel: "Credencial del modulo",
      credentialInputPlaceholder: "Pega API key o token para esta fuente",
      credentialConfigured: "Credencial configurada en servidor.",
      credentialRequiredMissing: "Este modulo requiere credencial. Agregala en este campo o en variables de entorno.",
      credentialOptionalHint: "Credencial opcional. Si la envias aqui se usa solo en esta solicitud.",
      discoveryNeedsCredential: "Falta credencial para este modulo.",
      sourceHintTelegram:
        "Modulo Telegram activo. Usa canales/grupos publicos o chats donde tu cuenta tenga acceso legitimo.",
      sourceHintGoogleMaps: "Google Maps activo. La busqueda usa Google Places API con filtros.",
      sourceHintOpenStreetMap:
        "OpenStreetMap activo. Discovery usa Nominatim y Overpass con filtros de negocio.",
      sourceHintReddit:
        "Reddit activo. Usa OAuth oficial cuando hay client_id/client_secret; si no, intenta endpoint publico.",
      sourceHintFoursquare: "Foursquare activo. Discovery usa Places API con filtros de negocio.",
      sourceHintYelp: "Yelp activo. Discovery usa Fusion API con filtros y ubicacion.",
      sourceHintTomTom: "TomTom activo. Discovery usa Search API con filtros de negocio.",
      sourceHintOpenCorporates:
        "OpenCorporates activo. Discovery usa API oficial de registros mercantiles.",
      filterPreviewEmpty: "Configura filtros y pulsa Aplicar.",
      previewTitle: "Resumen de filtros",
      previewPlatform: "Plataforma",
      previewQuery: "Busqueda",
      previewNiche: "Nicho",
      previewWebsite: "Web",
      previewPhone: "Telefono",
      previewLocation: "Ubicacion",
      previewRating: "Rating minimo",
      previewVerified: "Solo verificados",
      integrationTitle: "Estado de integracion",
      mapsActiveHint: "Google Maps discovery activo via Google Places API.",
      osmActiveHint: "OpenStreetMap discovery activo via Nominatim y Overpass.",
      redditActiveHint: "Reddit discovery activo con OAuth oficial (fallback publico).",
      foursquareActiveHint: "Foursquare discovery activo via Places API.",
      yelpActiveHint: "Yelp discovery activo via Fusion API oficial.",
      tomtomActiveHint: "TomTom discovery activo via Search API.",
      opencorporatesActiveHint:
        "OpenCorporates discovery activo via API oficial de registros mercantiles.",
      scrapeTitle: "Ejecutar scrape",
      singleTargetLabel: "Target unico (opcional)",
      singleTargetPlaceholder: "@canal o https://t.me/canal",
      backfillLabel: "Backfill historico (hasta el limite configurado)",
      dryRunLabel: "Solo dry-run (resuelve targets, no scrapea)",
      startScrapeBtn: "Iniciar scrape",
      scrapeHint: "Solo targets publicos o chats con acceso legitimo.",
      exportTitle: "Exportar mensajes",
      formatLabel: "Formato",
      downloadBtn: "Descargar export",
      exportHint: "Exporta la tabla completa de mensajes desde SQLite.",
      manualTitle: "Manual rapido",
      manualStep1: "Configura tus credenciales en `.env`.",
      manualStep2: "Define `targets` en `config.json`.",
      manualStep3: "Ejecuta `Dry-run` primero para validar acceso.",
      manualStep4: "Usa scrape incremental para operacion diaria.",
      manualStep5: "Usa backfill solo para historico inicial.",
      manualStep6: "Exporta CSV/JSON para analisis externo.",
      manualOpenLink: "Abrir manual completo",
      scrapeErrorTitle: "Error de scrape",
      summaryTitle: "Resumen de ultima ejecucion",
      summaryModeLabel: "Modo",
      summaryTargetsOkLabel: "Targets OK",
      summaryTargetsFailedLabel: "Targets fallidos",
      summaryNewMessagesLabel: "Mensajes nuevos",
      summaryFloodWaitsLabel: "Flood waits",
      dryInput: "Input",
      dryTargetId: "Target ID",
      dryResolved: "Resuelto",
      dryLastMessageId: "Ultimo Message ID",
      configuredTargetsTitle: "Targets configurados",
      noTargetsConfigured: "No hay targets configurados.",
      pathsTitle: "Rutas",
      targetsStatsTitle: "Estadisticas de targets",
      noTargetData: "Aun no hay datos de targets.",
      tableTarget: "Target",
      tableTargetId: "Target ID",
      tableMessages: "Mensajes",
      tableLastMessageId: "Ultimo Message ID",
      tableLastScrapedAt: "Ultimo scrapeo",
      recentRunsTitle: "Ejecuciones recientes",
      noRunsRegistered: "No hay ejecuciones registradas.",
      tableMode: "Modo",
      tableTargetFilter: "Filtro target",
      tableTargetsOk: "Targets OK",
      tableMessagesNew: "Mensajes nuevos",
      tableFloodWaits: "Flood waits",
      tableFinished: "Finalizado",
      discoveryColName: "Nombre",
      discoveryColWebsite: "Web",
      discoveryColPhone: "Telefono",
      discoveryColRating: "Rating",
      discoveryColLocation: "Ubicacion",
      discoveryColLink: "Enlace",
      discoveryRunning: "Ejecutando discovery...",
      discoveryDone: "Discovery finalizado. Resultados: {count}",
      discoveryError: "Error de discovery: {message}",
      discoveryNoData: "Sin resultados para los filtros actuales.",
      discoveryTelegramInfo: "Para Telegram usa el bloque Run Scrape (incremental/backfill/dry-run).",
      discoveryWarnings: "Ajustes automaticos: {warnings}",
      capNotSupported: "No soportado",
      capabilityTitle: "Capacidades",
      capabilityDiscoveryOn: "Discovery API: disponible",
      capabilityDiscoveryOff: "Discovery API: no disponible",
      capabilityLocationReq: "Ubicacion: requerida",
      capabilityLocationOpt: "Ubicacion: opcional",
      capabilityRatingOn: "Filtro rating: disponible",
      capabilityRatingOff: "Filtro rating: no disponible",
      capabilityVerifiedOn: "Filtro verificado: disponible",
      capabilityVerifiedOff: "Filtro verificado: no disponible",
      capabilityWebsiteOn: "Filtro web: disponible",
      capabilityWebsiteOff: "Filtro web: no disponible",
      capabilityPhoneOn: "Filtro telefono: disponible",
      capabilityPhoneOff: "Filtro telefono: no disponible",
      openLabel: "Abrir",
      noDataDash: "-",
    },
    en: {
      pageTitle: "Multi-Source Panel",
      navTitle: "Multi-Source Scraper",
      menuLabel: "Platforms",
      navTelegram: "Telegram",
      navGoogleMaps: "Google Maps",
      navOpenStreetMap: "OpenStreetMap",
      navReddit: "Reddit",
      navFoursquare: "Foursquare",
      navYelp: "Yelp",
      navTomTom: "TomTom",
      navOpenCorporates: "OpenCorporates",
      heroTitle: "Control and Discovery",
      heroLede: "Pick a source, set filters and run data collection safely.",
      languageLabel: "Language",
      themeLabel: "Color",
      langSpanish: "Spanish",
      langEnglish: "English",
      themeLight: "Light",
      themeDark: "Dark",
      metricTargetsDb: "Targets in DB",
      metricMessagesStored: "Messages Stored",
      metricConfigTargets: "Config Targets",
      sourceSearchTitle: "Source Search and Filters",
      sourceQueryLabel: "Search",
      sourceQueryPlaceholder: "Eg: vegan restaurants in Lima",
      sourceNicheLabel: "Business niche",
      nicheAll: "All niches",
      nicheRestaurants: "Restaurants",
      nicheRealEstate: "Real estate",
      nicheLegal: "Legal services",
      nicheMedical: "Medical clinics",
      nicheBeauty: "Beauty and wellness",
      sourceWebsiteLabel: "Has website",
      sourcePhoneLabel: "Has phone",
      filterAny: "Any",
      filterYes: "Yes",
      filterNo: "No",
      sourceLocationLabel: "Location",
      sourceLocationPlaceholder: "City or country",
      sourceRatingLabel: "Minimum rating",
      ratingAny: "Any",
      sourceVerifiedLabel: "Only verified profiles",
      applyFiltersBtn: "Apply filters",
      resetFiltersBtn: "Reset",
      credentialInputLabel: "Module credential",
      credentialInputPlaceholder: "Paste API key or token for this source",
      credentialConfigured: "Credential configured on server.",
      credentialRequiredMissing: "This module requires credentials. Add it here or in environment variables.",
      credentialOptionalHint: "Optional credential. If provided here, it is used only for this request.",
      discoveryNeedsCredential: "Missing credentials for this module.",
      sourceHintTelegram:
        "Telegram module is active. Use public channels/groups or chats where your account already has access.",
      sourceHintGoogleMaps: "Google Maps is active. Discovery runs with Google Places API and your filters.",
      sourceHintOpenStreetMap:
        "OpenStreetMap is active. Discovery runs with Nominatim and Overpass and your filters.",
      sourceHintReddit:
        "Reddit is active. Discovery uses official OAuth when client_id/client_secret are configured, with public fallback.",
      sourceHintFoursquare: "Foursquare is active. Discovery runs with Places API and your filters.",
      sourceHintYelp: "Yelp is active. Discovery runs with official Fusion API and your filters.",
      sourceHintTomTom: "TomTom is active. Discovery runs with Search API and your filters.",
      sourceHintOpenCorporates:
        "OpenCorporates is active. Discovery runs with official company registry API.",
      filterPreviewEmpty: "Configure filters and click Apply.",
      previewTitle: "Filter summary",
      previewPlatform: "Platform",
      previewQuery: "Search",
      previewNiche: "Niche",
      previewWebsite: "Website",
      previewPhone: "Phone",
      previewLocation: "Location",
      previewRating: "Minimum rating",
      previewVerified: "Only verified",
      integrationTitle: "Integration status",
      mapsActiveHint: "Google Maps discovery is active via Google Places API.",
      osmActiveHint: "OpenStreetMap discovery is active via Nominatim and Overpass.",
      redditActiveHint: "Reddit discovery is active with official OAuth (public fallback).",
      foursquareActiveHint: "Foursquare discovery is active via Places API.",
      yelpActiveHint: "Yelp discovery is active via official Fusion API.",
      tomtomActiveHint: "TomTom discovery is active via Search API.",
      opencorporatesActiveHint: "OpenCorporates discovery is active via official company registry API.",
      scrapeTitle: "Run scrape",
      singleTargetLabel: "Single target (optional)",
      singleTargetPlaceholder: "@channel or https://t.me/channel",
      backfillLabel: "Backfill history (up to configured limit)",
      dryRunLabel: "Dry-run only (resolve targets, do not scrape)",
      startScrapeBtn: "Start scrape",
      scrapeHint: "Only public targets or chats with legitimate access.",
      exportTitle: "Export messages",
      formatLabel: "Format",
      downloadBtn: "Download export",
      exportHint: "Exports the full messages table from SQLite.",
      manualTitle: "Quick manual",
      manualStep1: "Set your credentials in `.env`.",
      manualStep2: "Define `targets` in `config.json`.",
      manualStep3: "Run `Dry-run` first to validate access.",
      manualStep4: "Use incremental scrape for daily operation.",
      manualStep5: "Use backfill only for initial historical load.",
      manualStep6: "Export CSV/JSON for external analysis.",
      manualOpenLink: "Open full manual",
      scrapeErrorTitle: "Scrape error",
      summaryTitle: "Last run summary",
      summaryModeLabel: "Mode",
      summaryTargetsOkLabel: "Targets OK",
      summaryTargetsFailedLabel: "Targets failed",
      summaryNewMessagesLabel: "New messages",
      summaryFloodWaitsLabel: "Flood waits",
      dryInput: "Input",
      dryTargetId: "Target ID",
      dryResolved: "Resolved",
      dryLastMessageId: "Last Message ID",
      configuredTargetsTitle: "Configured targets",
      noTargetsConfigured: "No targets configured.",
      pathsTitle: "Paths",
      targetsStatsTitle: "Targets stats",
      noTargetData: "No target data yet.",
      tableTarget: "Target",
      tableTargetId: "Target ID",
      tableMessages: "Messages",
      tableLastMessageId: "Last Message ID",
      tableLastScrapedAt: "Last scraped at",
      recentRunsTitle: "Recent runs",
      noRunsRegistered: "No runs registered.",
      tableMode: "Mode",
      tableTargetFilter: "Target filter",
      tableTargetsOk: "Targets OK",
      tableMessagesNew: "Messages new",
      tableFloodWaits: "Flood waits",
      tableFinished: "Finished",
      discoveryColName: "Name",
      discoveryColWebsite: "Website",
      discoveryColPhone: "Phone",
      discoveryColRating: "Rating",
      discoveryColLocation: "Location",
      discoveryColLink: "Source link",
      discoveryRunning: "Running discovery...",
      discoveryDone: "Discovery finished. Results: {count}",
      discoveryError: "Discovery error: {message}",
      discoveryNoData: "No results for the current filters.",
      discoveryTelegramInfo: "For Telegram use the Run Scrape block (incremental/backfill/dry-run).",
      discoveryWarnings: "Automatic adjustments: {warnings}",
      capNotSupported: "Not supported",
      capabilityTitle: "Capabilities",
      capabilityDiscoveryOn: "Discovery API: available",
      capabilityDiscoveryOff: "Discovery API: unavailable",
      capabilityLocationReq: "Location: required",
      capabilityLocationOpt: "Location: optional",
      capabilityRatingOn: "Rating filter: available",
      capabilityRatingOff: "Rating filter: unavailable",
      capabilityVerifiedOn: "Verified filter: available",
      capabilityVerifiedOff: "Verified filter: unavailable",
      capabilityWebsiteOn: "Website filter: available",
      capabilityWebsiteOff: "Website filter: unavailable",
      capabilityPhoneOn: "Phone filter: available",
      capabilityPhoneOff: "Phone filter: unavailable",
      openLabel: "Open",
      noDataDash: "-",
    },
  };

  const platformMeta = {
    telegram: { labelKey: "navTelegram", hintKey: "sourceHintTelegram" },
    google_maps: { labelKey: "navGoogleMaps", hintKey: "sourceHintGoogleMaps" },
    reddit: { labelKey: "navReddit", hintKey: "sourceHintReddit" },
  };

  const defaultTheme = "light";
  const defaultPlatform = "telegram";
  const baseCapability = {
    supports_discovery_api: false,
    requires_location: false,
    supports_rating_filter: true,
    supports_verified_filter: true,
    supports_has_website_filter: true,
    supports_has_phone_filter: true,
    credential_required: false,
    credential_param: null,
    credential_env: null,
    credential_label: null,
    configured: true,
  };
  const fallbackCapabilities = {
    telegram: { ...baseCapability, supports_discovery_api: false, configured: true },
    google_maps: {
      ...baseCapability,
      supports_discovery_api: true,
      credential_required: true,
      credential_param: "api_key",
      credential_env: "GOOGLE_MAPS_API_KEY",
      credential_label: "Google Maps API Key",
      configured: false,
    },
    reddit: {
      ...baseCapability,
      supports_discovery_api: true,
      supports_rating_filter: false,
      credential_required: false,
      credential_param: "user_agent",
      credential_env: "REDDIT_USER_AGENT",
      credential_label: "Reddit User-Agent",
      oauth_envs: ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET"],
      oauth_configured: false,
      configured: true,
    },
  };

  const menuToggle = document.getElementById("menuToggle");
  const platformNav = document.getElementById("platformNav");
  const platformButtons = Array.from(document.querySelectorAll(".platform-link"));
  const platformPanels = Array.from(document.querySelectorAll(".platform-panel"));
  const platformBadge = document.getElementById("activePlatformBadge");
  const sourceHint = document.getElementById("sourceHint");
  const capabilityHint = document.getElementById("capabilityHint");

  const languageSelect = document.getElementById("languageSwitcher");
  const themeSelect = document.getElementById("themeSwitcher");
  const hasWebsiteSelect = document.getElementById("hasWebsite");
  const hasPhoneSelect = document.getElementById("hasPhone");
  const locationInput = document.getElementById("sourceLocation");
  const minRatingSelect = document.getElementById("minRating");
  const verifiedCheckbox = document.getElementById("onlyVerified");

  const sourceFilterForm = document.getElementById("sourceFilterForm");
  const resetFiltersBtn = document.getElementById("resetFiltersBtn");
  const filterPreview = document.getElementById("filterPreview");
  const discoveryFeedback = document.getElementById("discoveryFeedback");
  const discoveryResultsBody = document.getElementById("discoveryResultsBody");
  const credentialWrap = document.getElementById("moduleCredentialWrap");
  const credentialLabel = document.getElementById("moduleCredentialLabel");
  const credentialInput = document.getElementById("moduleCredentialInput");
  const credentialHelp = document.getElementById("moduleCredentialHelp");

  let currentLanguage = "es";
  let currentPlatform = defaultPlatform;
  let lastPayload = null;
  let capabilitiesByPlatform = { ...fallbackCapabilities };

  const getMessage = (key) => i18n[currentLanguage]?.[key] || i18n.es[key] || key;

  const formatTemplate = (template, vars) => {
    let output = template;
    Object.entries(vars).forEach(([key, value]) => {
      output = output.replace(`{${key}}`, String(value));
    });
    return output;
  };

  const getStoredLanguage = () => {
    const saved = localStorage.getItem("dashboard-language");
    if (saved === "es" || saved === "en") return saved;
    return navigator.language && navigator.language.toLowerCase().startsWith("es") ? "es" : "en";
  };

  const getCapabilities = (platform) => {
    const platformCapabilities = capabilitiesByPlatform[platform];
    if (!platformCapabilities) return { ...baseCapability };
    return { ...baseCapability, ...platformCapabilities };
  };

  const setFieldEnabled = (control, enabled) => {
    if (!control) return;
    control.disabled = !enabled;
    const field = control.closest(".source-field, .source-check");
    if (field) {
      field.classList.toggle("field-disabled", !enabled);
    }
  };

  const getCredentialStorageKey = (platform) => `dashboard-credential-${platform}`;

  const getCurrentCredential = (platform) => {
    if (!credentialInput) return "";
    if (platform === currentPlatform) {
      return credentialInput.value.trim();
    }
    return (localStorage.getItem(getCredentialStorageKey(platform)) || "").trim();
  };

  const renderCredentialState = () => {
    if (!credentialWrap || !credentialLabel || !credentialInput || !credentialHelp) return;
    const capabilities = getCapabilities(currentPlatform);
    const isTelegram = currentPlatform === "telegram";

    if (isTelegram || !capabilities.supports_discovery_api || !capabilities.credential_param) {
      credentialWrap.hidden = true;
      credentialInput.value = "";
      credentialHelp.textContent = "";
      return;
    }

    credentialWrap.hidden = false;
    credentialLabel.textContent = capabilities.credential_label || getMessage("credentialInputLabel");
    credentialInput.placeholder = getMessage("credentialInputPlaceholder");
    const saved = localStorage.getItem(getCredentialStorageKey(currentPlatform)) || "";
    credentialInput.value = saved;

    const hasServerCredential = Boolean(capabilities.configured);
    if (capabilities.credential_required) {
      credentialHelp.textContent = hasServerCredential
        ? getMessage("credentialConfigured")
        : getMessage("credentialRequiredMissing");
      credentialHelp.classList.toggle("error-text", !hasServerCredential && !saved.trim());
    } else {
      credentialHelp.textContent = hasServerCredential
        ? getMessage("credentialConfigured")
        : getMessage("credentialOptionalHint");
      credentialHelp.classList.remove("error-text");
    }
  };

  const renderCapabilityHint = () => {
    if (!capabilityHint) return;
    const capabilities = getCapabilities(currentPlatform);
    const lines = [
      `${getMessage("capabilityTitle")}:`,
      capabilities.supports_discovery_api ? getMessage("capabilityDiscoveryOn") : getMessage("capabilityDiscoveryOff"),
      capabilities.requires_location ? getMessage("capabilityLocationReq") : getMessage("capabilityLocationOpt"),
      capabilities.supports_rating_filter ? getMessage("capabilityRatingOn") : getMessage("capabilityRatingOff"),
      capabilities.supports_verified_filter
        ? getMessage("capabilityVerifiedOn")
        : getMessage("capabilityVerifiedOff"),
      capabilities.supports_has_website_filter
        ? getMessage("capabilityWebsiteOn")
        : getMessage("capabilityWebsiteOff"),
      capabilities.supports_has_phone_filter ? getMessage("capabilityPhoneOn") : getMessage("capabilityPhoneOff"),
      capabilities.credential_required ? getMessage("credentialInputLabel") : "",
    ];
    capabilityHint.textContent = lines.filter(Boolean).join(" | ");
  };

  const applyCapabilityState = () => {
    const capabilities = getCapabilities(currentPlatform);
    const isTelegram = currentPlatform === "telegram";

    const ratingEnabled = isTelegram || capabilities.supports_rating_filter;
    const verifiedEnabled = isTelegram || capabilities.supports_verified_filter;
    const websiteEnabled = isTelegram || capabilities.supports_has_website_filter;
    const phoneEnabled = isTelegram || capabilities.supports_has_phone_filter;

    setFieldEnabled(minRatingSelect, ratingEnabled);
    setFieldEnabled(verifiedCheckbox, verifiedEnabled);
    setFieldEnabled(hasWebsiteSelect, websiteEnabled);
    setFieldEnabled(hasPhoneSelect, phoneEnabled);

    if (!ratingEnabled && minRatingSelect) {
      minRatingSelect.value = "0";
    }
    if (!verifiedEnabled && verifiedCheckbox) {
      verifiedCheckbox.checked = false;
    }
    if (!websiteEnabled && hasWebsiteSelect) {
      hasWebsiteSelect.value = "any";
    }
    if (!phoneEnabled && hasPhoneSelect) {
      hasPhoneSelect.value = "any";
    }

    if (locationInput) {
      locationInput.required = !isTelegram && Boolean(capabilities.requires_location);
      locationInput.setAttribute("aria-required", locationInput.required ? "true" : "false");
    }

    renderCapabilityHint();
    renderCredentialState();
  };

  const loadCapabilities = async () => {
    try {
      const response = await fetch("/api/capabilities", { method: "GET" });
      if (!response.ok) return;
      const payload = await response.json();
      const platforms = payload && typeof payload === "object" ? payload.platforms : null;
      if (!platforms || typeof platforms !== "object") return;
      capabilitiesByPlatform = { ...fallbackCapabilities, ...platforms };
    } catch (_) {
      capabilitiesByPlatform = { ...fallbackCapabilities };
    }
  };

  const applyLanguage = (lang) => {
    currentLanguage = i18n[lang] ? lang : "es";
    document.documentElement.lang = currentLanguage;

    document.querySelectorAll("[data-i18n]").forEach((element) => {
      const key = element.getAttribute("data-i18n");
      if (!key) return;
      const value = getMessage(key);
      if (element.tagName.toLowerCase() === "title") {
        document.title = value;
      } else {
        element.textContent = value;
      }
    });

    document.querySelectorAll("[data-i18n-placeholder]").forEach((element) => {
      const key = element.getAttribute("data-i18n-placeholder");
      if (!key) return;
      element.setAttribute("placeholder", getMessage(key));
    });

    refreshPlatformLabels();
    renderCapabilityHint();
    renderCredentialState();
    renderFilterPreview();
  };

  const normalizeTheme = (theme) => {
    if (theme === "dark" || theme === "graphite") return "dark";
    if (theme === "light" || theme === "ocean" || theme === "amber") return "light";
    return defaultTheme;
  };

  const applyTheme = (theme) => {
    const selected = normalizeTheme(theme);
    document.documentElement.setAttribute("data-theme", selected);
    return selected;
  };

  const refreshPlatformLabels = () => {
    const meta = platformMeta[currentPlatform] || platformMeta[defaultPlatform];
    if (platformBadge) {
      platformBadge.textContent = getMessage(meta.labelKey);
    }
    if (sourceHint) {
      sourceHint.textContent = getMessage(meta.hintKey);
    }
  };

  const setPlatform = (platform) => {
    const selected = platformMeta[platform] ? platform : defaultPlatform;
    currentPlatform = selected;
    localStorage.setItem("dashboard-platform", selected);

    platformButtons.forEach((button) => {
      const isActive = button.dataset.platform === selected;
      button.classList.toggle("is-active", isActive);
      button.setAttribute("aria-pressed", isActive ? "true" : "false");
    });

    platformPanels.forEach((panel) => {
      panel.hidden = panel.dataset.platform !== selected;
    });

    refreshPlatformLabels();
    applyCapabilityState();
    renderFilterPreview();
  };

  const boolLabel = (value) => (value ? getMessage("filterYes") : getMessage("filterNo"));

  const renderFilterPreview = () => {
    if (!filterPreview) return;
    if (!lastPayload) {
      filterPreview.textContent = getMessage("filterPreviewEmpty");
      return;
    }
    const capabilities = getCapabilities(lastPayload.platform);
    const ratingValue = capabilities.supports_rating_filter ? lastPayload.minRating : getMessage("capNotSupported");
    const verifiedValue = capabilities.supports_verified_filter
      ? boolLabel(lastPayload.onlyVerified)
      : getMessage("capNotSupported");

    const lines = [
      `${getMessage("previewTitle")}:`,
      `${getMessage("previewPlatform")}: ${getMessage(platformMeta[lastPayload.platform].labelKey)}`,
      `${getMessage("previewQuery")}: ${lastPayload.query || "-"}`,
      `${getMessage("previewNiche")}: ${lastPayload.nicheLabel || lastPayload.niche}`,
      `${getMessage("previewWebsite")}: ${lastPayload.hasWebsite}`,
      `${getMessage("previewPhone")}: ${lastPayload.hasPhone}`,
      `${getMessage("previewLocation")}: ${lastPayload.location || "-"}`,
      `${getMessage("previewRating")}: ${ratingValue}`,
      `${getMessage("previewVerified")}: ${verifiedValue}`,
    ];

    filterPreview.textContent = lines.join("\n");
  };

  const buildPayload = () => {
    const query = document.getElementById("sourceQuery")?.value.trim() || "";
    const nicheRaw = document.getElementById("sourceNiche")?.value || "all";
    const hasWebsiteRaw = document.getElementById("hasWebsite")?.value || "any";
    const hasPhoneRaw = document.getElementById("hasPhone")?.value || "any";
    const location = document.getElementById("sourceLocation")?.value.trim() || "";
    const minRatingRaw = document.getElementById("minRating")?.value || "0";
    const onlyVerified = Boolean(document.getElementById("onlyVerified")?.checked);

    const nicheLabel =
      document.querySelector(`#sourceNiche option[value="${nicheRaw}"]`)?.textContent?.trim() || nicheRaw;
    const hasWebsiteLabel =
      document.querySelector(`#hasWebsite option[value="${hasWebsiteRaw}"]`)?.textContent?.trim() || hasWebsiteRaw;
    const hasPhoneLabel =
      document.querySelector(`#hasPhone option[value="${hasPhoneRaw}"]`)?.textContent?.trim() || hasPhoneRaw;
    const capabilities = getCapabilities(currentPlatform);
    const credentialValue = getCurrentCredential(currentPlatform);
    const credentials = {};
    if (capabilities.credential_param && credentialValue) {
      credentials[capabilities.credential_param] = credentialValue;
    }

    return {
      platform: currentPlatform,
      query,
      niche: nicheRaw,
      nicheLabel,
      hasWebsite: hasWebsiteLabel,
      hasPhone: hasPhoneLabel,
      location,
      minRating: minRatingRaw,
      onlyVerified,
      niche_raw: nicheRaw,
      has_website: hasWebsiteRaw,
      has_phone: hasPhoneRaw,
      min_rating: minRatingRaw,
      only_verified: onlyVerified,
      limit: 20,
      credentials,
    };
  };

  const setFeedback = (message, type) => {
    if (!discoveryFeedback) return;
    discoveryFeedback.textContent = message;
    discoveryFeedback.classList.remove("feedback-ok", "feedback-error");
    if (type === "ok") discoveryFeedback.classList.add("feedback-ok");
    if (type === "error") discoveryFeedback.classList.add("feedback-error");
  };

  const renderResults = (items) => {
    if (!discoveryResultsBody) return;
    discoveryResultsBody.innerHTML = "";
    if (!items || items.length === 0) {
      const tr = document.createElement("tr");
      const td = document.createElement("td");
      td.colSpan = 6;
      td.textContent = getMessage("discoveryNoData");
      tr.appendChild(td);
      discoveryResultsBody.appendChild(tr);
      return;
    }

    items.forEach((item) => {
      const tr = document.createElement("tr");
      const nameCell = document.createElement("td");
      nameCell.textContent = item.name || getMessage("noDataDash");

      const websiteCell = document.createElement("td");
      if (item.website) {
        const link = document.createElement("a");
        link.href = item.website;
        link.target = "_blank";
        link.rel = "noopener";
        link.textContent = item.website;
        websiteCell.appendChild(link);
      } else {
        websiteCell.textContent = getMessage("noDataDash");
      }

      const phoneCell = document.createElement("td");
      phoneCell.textContent = item.phone || getMessage("noDataDash");

      const ratingCell = document.createElement("td");
      ratingCell.textContent = item.rating ?? getMessage("noDataDash");

      const locationCell = document.createElement("td");
      locationCell.textContent = item.location || getMessage("noDataDash");

      const sourceLinkCell = document.createElement("td");
      if (item.url) {
        const link = document.createElement("a");
        link.href = item.url;
        link.target = "_blank";
        link.rel = "noopener";
        link.textContent = getMessage("openLabel");
        sourceLinkCell.appendChild(link);
      } else {
        sourceLinkCell.textContent = getMessage("noDataDash");
      }

      tr.appendChild(nameCell);
      tr.appendChild(websiteCell);
      tr.appendChild(phoneCell);
      tr.appendChild(ratingCell);
      tr.appendChild(locationCell);
      tr.appendChild(sourceLinkCell);
      discoveryResultsBody.appendChild(tr);
    });
  };

  const runDiscovery = async (payload) => {
    if (payload.platform === "telegram") {
      setFeedback(getMessage("discoveryTelegramInfo"), "ok");
      renderResults([]);
      return;
    }
    const capabilities = getCapabilities(payload.platform);
    if (capabilities.requires_location && !String(payload.location || "").trim()) {
      setFeedback(
        formatTemplate(getMessage("discoveryError"), {
          message: getMessage("capabilityLocationReq"),
        }),
        "error"
      );
      renderResults([]);
      return;
    }
    if (
      capabilities.credential_required &&
      !capabilities.configured &&
      !((payload.credentials || {})[capabilities.credential_param || ""])
    ) {
      setFeedback(
        formatTemplate(getMessage("discoveryError"), {
          message: getMessage("discoveryNeedsCredential"),
        }),
        "error"
      );
      renderResults([]);
      return;
    }

    setFeedback(getMessage("discoveryRunning"), "ok");
    try {
      const response = await fetch("/api/discover", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      if (!response.ok || data.status !== "ok") {
        const baseMessage = data.message || "unknown error";
        const warningText =
          Array.isArray(data.warnings) && data.warnings.length > 0
            ? ` ${formatTemplate(getMessage("discoveryWarnings"), { warnings: data.warnings.join(" | ") })}`
            : "";
        setFeedback(formatTemplate(getMessage("discoveryError"), { message: `${baseMessage}${warningText}` }), "error");
        renderResults([]);
        return;
      }

      let message = formatTemplate(getMessage("discoveryDone"), { count: data.count || 0 });
      if (Array.isArray(data.warnings) && data.warnings.length > 0) {
        message += ` ${formatTemplate(getMessage("discoveryWarnings"), { warnings: data.warnings.join(" | ") })}`;
      }
      setFeedback(message, "ok");
      renderResults(data.items || []);
    } catch (error) {
      setFeedback(
        formatTemplate(getMessage("discoveryError"), {
          message: error instanceof Error ? error.message : "request failed",
        }),
        "error"
      );
      renderResults([]);
    }
  };

  if (menuToggle && platformNav) {
    menuToggle.addEventListener("click", () => {
      const isOpen = platformNav.classList.toggle("is-open");
      menuToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });
  }

  platformButtons.forEach((button) => {
    button.addEventListener("click", () => {
      setPlatform(button.dataset.platform || defaultPlatform);
      if (platformNav && platformNav.classList.contains("is-open")) {
        platformNav.classList.remove("is-open");
        menuToggle?.setAttribute("aria-expanded", "false");
      }
    });
  });

  if (credentialInput) {
    credentialInput.addEventListener("input", () => {
      localStorage.setItem(getCredentialStorageKey(currentPlatform), credentialInput.value);
      renderCredentialState();
    });
  }

  if (sourceFilterForm) {
    sourceFilterForm.addEventListener("submit", (event) => {
      event.preventDefault();
      const payload = buildPayload();
      lastPayload = payload;
      renderFilterPreview();
      runDiscovery(payload);
    });
  }

  if (resetFiltersBtn && sourceFilterForm) {
    resetFiltersBtn.addEventListener("click", () => {
      sourceFilterForm.reset();
      lastPayload = null;
      renderFilterPreview();
      setFeedback("", "");
      renderResults([]);
    });
  }

  const initialLanguage = getStoredLanguage();
  const initialTheme = localStorage.getItem("dashboard-theme") || defaultTheme;
  const initialPlatform = localStorage.getItem("dashboard-platform") || defaultPlatform;

  if (languageSelect) {
    languageSelect.value = initialLanguage;
    languageSelect.addEventListener("change", (event) => {
      const lang = event.target.value;
      localStorage.setItem("dashboard-language", lang);
      applyLanguage(lang);
    });
  }

  if (themeSelect) {
    themeSelect.value = normalizeTheme(initialTheme);
    themeSelect.addEventListener("change", (event) => {
      const theme = normalizeTheme(event.target.value);
      localStorage.setItem("dashboard-theme", theme);
      applyTheme(theme);
      event.target.value = theme;
    });
  }

  const initialize = async () => {
    await loadCapabilities();
    applyTheme(initialTheme);
    setPlatform(initialPlatform);
    applyLanguage(initialLanguage);
    renderResults([]);
  };

  initialize();
})();
