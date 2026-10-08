(() => {
  const BLUE = "#2457f5";
  const MUTED = "#8c948f";
  const INK = "#121c2b";
  const PAPER = "#f3efe6";

  const render = (figure) => {
    const target = figure.querySelector(".article-cost-comparison__plot");
    const primary = figure.dataset.primary;
    const points = [...figure.querySelectorAll("[data-cost-point]")].map((row) => ({
      id: row.dataset.id,
      label: row.dataset.label,
      cost: Number.parseFloat(row.dataset.cost),
      coverage: Number.parseFloat(row.dataset.coverage),
      attempts: Number.parseInt(row.dataset.attempts, 10),
    }));
    const currency = new Intl.NumberFormat(document.documentElement.lang || "en", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    });
    const formatCost = (value) => document.documentElement.lang.startsWith("fr")
      ? `${currency.format(value)} $`
      : `$${currency.format(value)}`;
    const width = Math.max(320, Math.floor(target.getBoundingClientRect().width));
    const compact = width < 560;
    const chart = Plot.plot({
      width,
      height: compact ? 300 : 330,
      marginTop: 25,
      marginRight: compact ? 58 : 90,
      marginBottom: 60,
      marginLeft: compact ? 112 : 205,
      x: {
        domain: [0, Math.max(...points.map((point) => point.cost)) * 1.08],
        label: figure.dataset.xLabel,
        grid: true,
        tickFormat: (value) => `$${Math.round(value)}`,
      },
      y: { domain: points.map((point) => point.label), label: null },
      marks: [
        Plot.frame({ stroke: INK, strokeOpacity: 0.5 }),
        Plot.barX(points, {
          x: "cost",
          y: "label",
          fill: (point) => point.id === primary ? BLUE : MUTED,
          fillOpacity: (point) => point.id === primary ? 1 : 0.55,
          channels: {
            scenario: { value: "label", label: figure.dataset.scenarioLabel },
            costLabel: { value: (point) => formatCost(point.cost), label: figure.dataset.costLabel },
            coverage: { value: (point) => `${point.coverage}${figure.dataset.coverageSuffix}`, label: figure.dataset.coverageLabel },
            attempts: { value: "attempts", label: figure.dataset.attemptsLabel },
          },
          tip: { format: { x: false, y: false, fill: false, fillOpacity: false } },
        }),
        Plot.text(points, {
          x: "cost",
          y: "label",
          text: (point) => formatCost(point.cost),
          dx: 8,
          textAnchor: "start",
          fontWeight: 800,
          fill: (point) => point.id === primary ? BLUE : INK,
        }),
      ],
    });
    chart.querySelectorAll("style").forEach((style) => style.remove());
    chart.setAttribute("role", "img");
    chart.setAttribute("aria-labelledby", `${target.id}-title`);
    chart.setAttribute("aria-describedby", `${target.id}-description`);
    target.replaceChildren(chart);
  };

  document.querySelectorAll("[data-cost-comparison]").forEach((figure) => {
    let frame;
    const refresh = () => {
      window.cancelAnimationFrame(frame);
      frame = window.requestAnimationFrame(() => render(figure));
    };
    refresh();
    new ResizeObserver(refresh).observe(figure.querySelector(".article-cost-comparison__plot"));
  });
})();
