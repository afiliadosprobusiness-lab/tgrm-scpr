(() => {
  const i18n = {
    es: {
      pageTitle: "Panel Telegram Scraper",
      heroTitle: "Panel de Control",
      heroLede: "Ejecuta scraping incremental, dry-run, backfill y exportes desde esta interfaz.",
      languageLabel: "Idioma",
      themeLabel: "Color",
      langSpanish: "Español",
      langEnglish: "English",
      themeOcean: "Océano",
      themeAmber: "Ámbar",
      themeGraphite: "Grafito",
      metricTargetsDb: "Targets en DB",
      metricMessagesStored: "Mensajes guardados",
      metricConfigTargets: "Targets configurados",
      scrapeTitle: "Ejecutar Scrape",
      singleTargetLabel: "Target único (opcional)",
      singleTargetPlaceholder: "@canal o https://t.me/canal",
      backfillLabel: "Backfill histórico (hasta el límite configurado)",
      dryRunLabel: "Solo dry-run (resuelve targets, no scrapea)",
      startScrapeBtn: "Iniciar Scrape",
      scrapeHint: "Solo soporta targets públicos o chats a los que tu cuenta tenga acceso legítimo.",
      exportTitle: "Exportar Mensajes",
      formatLabel: "Formato",
      downloadBtn: "Descargar Export",
      exportHint: "Exporta toda la tabla de mensajes desde SQLite.",
      manualTitle: "Manual rápido",
      manualStep1: "Configura tus credenciales en `.env`.",
      manualStep2: "Define `targets` en `config.json`.",
      manualStep3: "Primero ejecuta `Dry-run` para validar accesos.",
      manualStep4: "Ejecuta scrape incremental sin backfill para uso diario.",
      manualStep5: "Usa backfill solo cuando necesites histórico inicial.",
      manualStep6: "Exporta en CSV/JSON cuando necesites análisis externo.",
      manualOpenLink: "Abrir manual completo",
      scrapeErrorTitle: "Error de Scrape",
      summaryTitle: "Resumen de última ejecución",
      summaryModeLabel: "Modo",
      summaryTargetsOkLabel: "Targets OK",
      summaryTargetsFailedLabel: "Targets fallidos",
      summaryNewMessagesLabel: "Mensajes nuevos",
      summaryFloodWaitsLabel: "Flood waits",
      dryInput: "Input",
      dryTargetId: "Target ID",
      dryResolved: "Resuelto",
      dryLastMessageId: "Último Message ID",
      configuredTargetsTitle: "Targets configurados",
      noTargetsConfigured: "No hay targets configurados.",
      pathsTitle: "Rutas",
      targetsStatsTitle: "Estadísticas de targets",
      noTargetData: "Aún no hay datos de targets.",
      tableTarget: "Target",
      tableTargetId: "Target ID",
      tableMessages: "Mensajes",
      tableLastMessageId: "Último Message ID",
      tableLastScrapedAt: "Último scrapeo",
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
      pageTitle: "Telegram Scraper Dashboard",
      heroTitle: "Scraper Control Panel",
      heroLede: "Run incremental scraping, dry-run, backfill and exports from this dashboard.",
      languageLabel: "Language",
      themeLabel: "Color Theme",
      langSpanish: "Spanish",
      langEnglish: "English",
      themeOcean: "Ocean",
      themeAmber: "Amber",
      themeGraphite: "Graphite",
      metricTargetsDb: "Targets in DB",
      metricMessagesStored: "Messages Stored",
      metricConfigTargets: "Config Targets",
      scrapeTitle: "Run Scrape",
      singleTargetLabel: "Single target (optional)",
      singleTargetPlaceholder: "@channel or https://t.me/channel",
      backfillLabel: "Backfill history (up to configured limit)",
      dryRunLabel: "Dry-run only (resolve targets, do not scrape)",
      startScrapeBtn: "Start Scrape",
      scrapeHint: "Supports public targets or chats your account can access legitimately.",
      exportTitle: "Export Messages",
      formatLabel: "Format",
      downloadBtn: "Download Export",
      exportHint: "Exports the full messages table from SQLite.",
      manualTitle: "Quick Manual",
      manualStep1: "Set your credentials in `.env`.",
      manualStep2: "Define `targets` in `config.json`.",
      manualStep3: "Run `Dry-run` first to validate access.",
      manualStep4: "Run incremental scrape without backfill for day-to-day usage.",
      manualStep5: "Use backfill only for initial historical load.",
      manualStep6: "Export as CSV/JSON when you need external analysis.",
      manualOpenLink: "Open full manual",
      scrapeErrorTitle: "Scrape Error",
      summaryTitle: "Last Run Summary",
      summaryModeLabel: "Mode",
      summaryTargetsOkLabel: "Targets OK",
      summaryTargetsFailedLabel: "Targets Failed",
      summaryNewMessagesLabel: "New Messages",
      summaryFloodWaitsLabel: "Flood Waits",
      dryInput: "Input",
      dryTargetId: "Target ID",
      dryResolved: "Resolved",
      dryLastMessageId: "Last Message ID",
      configuredTargetsTitle: "Configured Targets",
      noTargetsConfigured: "No targets configured.",
      pathsTitle: "Paths",
      targetsStatsTitle: "Targets Stats",
      noTargetData: "No target data yet.",
      tableTarget: "Target",
      tableTargetId: "Target ID",
      tableMessages: "Messages",
      tableLastMessageId: "Last Message ID",
      tableLastScrapedAt: "Last Scraped At",
      recentRunsTitle: "Recent Runs",
      noRunsRegistered: "No runs registered.",
      tableMode: "Mode",
      tableTargetFilter: "Target Filter",
      tableTargetsOk: "Targets OK",
      tableMessagesNew: "Messages New",
      tableFloodWaits: "Flood Waits",
      tableFinished: "Finished",
    },
  };

  const defaultTheme = "ocean";
  const languageSelect = document.getElementById("languageSwitcher");
  const themeSelect = document.getElementById("themeSwitcher");

  const getStoredLanguage = () => {
    const saved = localStorage.getItem("dashboard-language");
    if (saved === "es" || saved === "en") return saved;
    return navigator.language && navigator.language.toLowerCase().startsWith("es") ? "es" : "en";
  };

  const applyLanguage = (lang) => {
    const selected = i18n[lang] ? lang : "es";
    const messages = i18n[selected];
    document.documentElement.lang = selected;

    document.querySelectorAll("[data-i18n]").forEach((element) => {
      const key = element.getAttribute("data-i18n");
      if (!key || !messages[key]) return;
      if (element.tagName.toLowerCase() === "title") {
        document.title = messages[key];
      } else {
        element.textContent = messages[key];
      }
    });

    document.querySelectorAll("[data-i18n-placeholder]").forEach((element) => {
      const key = element.getAttribute("data-i18n-placeholder");
      if (!key || !messages[key]) return;
      element.setAttribute("placeholder", messages[key]);
    });
  };

  const applyTheme = (theme) => {
    const selected = theme === "amber" || theme === "graphite" ? theme : defaultTheme;
    document.documentElement.setAttribute("data-theme", selected);
  };

  const initialLanguage = getStoredLanguage();
  const initialTheme = localStorage.getItem("dashboard-theme") || defaultTheme;

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
  applyLanguage(initialLanguage);
})();

