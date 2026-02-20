(() => {
  const i18n = {
    es: {
      pageTitle: "Panel Multi-Fuente",
      navTitle: "Scraper Multi-Fuente",
      menuLabel: "Plataformas",
      navTelegram: "Telegram",
      navGoogleMaps: "Google Maps",
      navInstagram: "Instagram",
      navReddit: "Reddit",
      heroTitle: "Control y Descubrimiento",
      heroLede: "Elige una fuente, define filtros y ejecuta recoleccion de datos de forma segura.",
      languageLabel: "Idioma",
      themeLabel: "Color",
      langSpanish: "Espanol",
      langEnglish: "English",
      themeOcean: "Oceano",
      themeAmber: "Ambar",
      themeGraphite: "Grafito",
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
      sourceHintTelegram:
        "Modulo Telegram activo. Usa canales/grupos publicos o chats donde tu cuenta tenga acceso legitimo.",
      sourceHintGoogleMaps:
        "Google Maps aun no esta conectado. Puedes preparar filtros de nicho, web y telefono para futura integracion.",
      sourceHintInstagram:
        "Instagram aun no esta conectado. El formulario queda listo para cuando se habilite el conector.",
      sourceHintReddit:
        "Reddit aun no esta conectado. Define filtros y deja listo el criterio de busqueda.",
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
      mapsComingSoon:
        "El scraper de Google Maps no esta activo aun. La UI de filtros ya esta lista para definir nicho, web y telefono.",
      instagramComingSoon:
        "El scraper de Instagram no esta activo aun. La UI esta lista y falta conectar backend con reglas de cumplimiento.",
      redditComingSoon:
        "El scraper de Reddit no esta activo aun. Puedes preparar filtros y conectar el adaptador despues.",
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
    },
    en: {
      pageTitle: "Multi-Source Scraper Panel",
      navTitle: "Multi-Source Scraper",
      menuLabel: "Platforms",
      navTelegram: "Telegram",
      navGoogleMaps: "Google Maps",
      navInstagram: "Instagram",
      navReddit: "Reddit",
      heroTitle: "Control and Discovery",
      heroLede: "Pick a source, set filters and run data collection safely.",
      languageLabel: "Language",
      themeLabel: "Color",
      langSpanish: "Spanish",
      langEnglish: "English",
      themeOcean: "Ocean",
      themeAmber: "Amber",
      themeGraphite: "Graphite",
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
      sourceHintTelegram:
        "Telegram module is active. Use public channels/groups or chats where your account already has access.",
      sourceHintGoogleMaps:
        "Google Maps is not connected yet. You can prepare niche, website and phone filters for future integration.",
      sourceHintInstagram:
        "Instagram is not connected yet. The form is ready while backend integration is pending.",
      sourceHintReddit:
        "Reddit is not connected yet. Define filters now and connect the source adapter later.",
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
      mapsComingSoon:
        "Google Maps scraper is not active yet. Filter UI is ready for niche, website and phone selection.",
      instagramComingSoon:
        "Instagram scraper is not active yet. UI is ready while backend and compliance rules are pending.",
      redditComingSoon:
        "Reddit scraper is not active yet. You can define filters now and connect an adapter later.",
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
    },
  };

  const platformMeta = {
    telegram: { labelKey: "navTelegram", hintKey: "sourceHintTelegram" },
    google_maps: { labelKey: "navGoogleMaps", hintKey: "sourceHintGoogleMaps" },
    instagram: { labelKey: "navInstagram", hintKey: "sourceHintInstagram" },
    reddit: { labelKey: "navReddit", hintKey: "sourceHintReddit" },
  };

  const defaultTheme = "ocean";
  const defaultPlatform = "telegram";

  const menuToggle = document.getElementById("menuToggle");
  const platformNav = document.getElementById("platformNav");
  const platformButtons = Array.from(document.querySelectorAll(".platform-link"));
  const platformPanels = Array.from(document.querySelectorAll(".platform-panel"));
  const platformBadge = document.getElementById("activePlatformBadge");
  const sourceHint = document.getElementById("sourceHint");

  const languageSelect = document.getElementById("languageSwitcher");
  const themeSelect = document.getElementById("themeSwitcher");

  const sourceFilterForm = document.getElementById("sourceFilterForm");
  const resetFiltersBtn = document.getElementById("resetFiltersBtn");
  const filterPreview = document.getElementById("filterPreview");

  let currentLanguage = "es";
  let currentPlatform = defaultPlatform;
  let lastPayload = null;

  const getMessage = (key) => i18n[currentLanguage]?.[key] || i18n.es[key] || key;

  const getStoredLanguage = () => {
    const saved = localStorage.getItem("dashboard-language");
    if (saved === "es" || saved === "en") return saved;
    return navigator.language && navigator.language.toLowerCase().startsWith("es") ? "es" : "en";
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
    renderFilterPreview();
  };

  const applyTheme = (theme) => {
    const selected = theme === "amber" || theme === "graphite" ? theme : defaultTheme;
    document.documentElement.setAttribute("data-theme", selected);
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
  };

  const boolLabel = (value) => (value ? getMessage("filterYes") : getMessage("filterNo"));

  const renderFilterPreview = () => {
    if (!filterPreview) return;
    if (!lastPayload) {
      filterPreview.textContent = getMessage("filterPreviewEmpty");
      return;
    }

    const lines = [
      `${getMessage("previewTitle")}:`,
      `${getMessage("previewPlatform")}: ${getMessage(platformMeta[lastPayload.platform].labelKey)}`,
      `${getMessage("previewQuery")}: ${lastPayload.query || "-"}`,
      `${getMessage("previewNiche")}: ${lastPayload.niche}`,
      `${getMessage("previewWebsite")}: ${lastPayload.hasWebsite}`,
      `${getMessage("previewPhone")}: ${lastPayload.hasPhone}`,
      `${getMessage("previewLocation")}: ${lastPayload.location || "-"}`,
      `${getMessage("previewRating")}: ${lastPayload.minRating}`,
      `${getMessage("previewVerified")}: ${boolLabel(lastPayload.onlyVerified)}`,
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

    return {
      platform: currentPlatform,
      query,
      niche: nicheLabel,
      hasWebsite: hasWebsiteLabel,
      hasPhone: hasPhoneLabel,
      location,
      minRating: minRatingRaw,
      onlyVerified,
    };
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

  if (sourceFilterForm) {
    sourceFilterForm.addEventListener("submit", (event) => {
      event.preventDefault();
      lastPayload = buildPayload();
      renderFilterPreview();
    });
  }

  if (resetFiltersBtn && sourceFilterForm) {
    resetFiltersBtn.addEventListener("click", () => {
      sourceFilterForm.reset();
      lastPayload = null;
      renderFilterPreview();
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
    themeSelect.value = initialTheme;
    themeSelect.addEventListener("change", (event) => {
      const theme = event.target.value;
      localStorage.setItem("dashboard-theme", theme);
      applyTheme(theme);
    });
  }

  applyTheme(initialTheme);
  setPlatform(initialPlatform);
  applyLanguage(initialLanguage);
})();
