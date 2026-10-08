(() => {
  const COLORS = {
    ink: "#121c2b",
    paper: "#f3efe6",
    blue: "#2457f5",
    coral: "#ff5a4e",
    muted: "#8c948f",
    line: "rgba(18,28,43,.18)",
  };

  const number = (value) => Number.parseFloat(value);

  const paretoFrontier = (points) => {
    let bestY = Number.NEGATIVE_INFINITY;
    return [...points]
      .sort((left, right) => left.x - right.x || right.y - left.y)
      .filter((point) => {
        if (point.y <= bestY) return false;
        bestY = point.y;
        return true;
      });
  };

  const linearModel = (points) => {
    const meanX = points.reduce((sum, point) => sum + point.x, 0) / points.length;
    const meanY = points.reduce((sum, point) => sum + point.y, 0) / points.length;
    const covariance = points.reduce(
      (sum, point) => sum + (point.x - meanX) * (point.y - meanY),
      0,
    );
    const variance = points.reduce(
      (sum, point) => sum + (point.x - meanX) ** 2,
      0,
    );
    const slope = variance === 0 ? 0 : covariance / variance;
    const intercept = meanY - slope * meanX;
    return { predict: (x) => intercept + slope * x };
  };

  const render = (figure) => {
    const target = figure.querySelector(".article-scatter-chart__plot");
    const rows = [...figure.querySelectorAll("[data-chart-point]")];
    const excluded = new Set(
      figure.dataset.regressionExclude.split(",").map((value) => value.trim()).filter(Boolean),
    );
    const points = rows.map((row) => ({
      id: row.dataset.id,
      label: row.dataset.label,
      x: number(row.dataset.x),
      y: number(row.dataset.y),
      attempts: number(row.dataset.attempts),
    }));
    const regressionPoints = points.filter((point) => !excluded.has(point.id));
    const model = linearModel(regressionPoints);
    const primary = figure.dataset.primary;
    const secondary = figure.dataset.secondary;
    const reference = figure.dataset.reference;
    const xSuffix = figure.dataset.xTotal ? `/${figure.dataset.xTotal}` : "";
    const ySuffix = figure.dataset.yTotal ? `/${figure.dataset.yTotal}` : "";
    const currency = new Intl.NumberFormat(document.documentElement.lang || "en", {
      style: "currency",
      currency: "USD",
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    });
    const formatX = (value) => figure.dataset.xFormat === "currency"
      ? currency.format(value)
      : `${value}${xSuffix}`;

    for (const point of points) {
      point.group = point.id === primary
        ? "primary"
        : point.id === secondary
          ? "secondary"
          : point.id === reference
            ? "reference"
            : "default";
      point.residual = point.y - model.predict(point.x);
      point.symbol = point.group === "secondary"
        ? "diamond"
        : point.group === "reference"
          ? "square"
          : "circle";
      point.color = point.group === "primary"
        ? COLORS.blue
        : point.group === "secondary"
          ? COLORS.coral
          : point.group === "reference"
            ? COLORS.ink
            : COLORS.muted;
    }

    const width = Math.max(320, Math.floor(target.getBoundingClientRect().width));
    const compact = width < 560;
    const emphasized = points.filter((point) => point.group !== "default");
    const primaryPoint = points.filter((point) => point.group === "primary");
    const secondaryPoint = points.filter((point) => point.group === "secondary");
    const referencePoint = points.filter((point) => point.group === "reference");
    const marks = [
      Plot.frame({ stroke: COLORS.ink, strokeOpacity: 0.5 }),
    ];

    if (figure.dataset.regression === "linear") {
      marks.push(Plot.linearRegressionY(regressionPoints, {
        x: "x",
        y: "y",
        stroke: COLORS.blue,
        strokeWidth: 2,
        fill: COLORS.blue,
        fillOpacity: 0.08,
      }));
    }

    if (figure.dataset.frontier === "upper-left") {
      const frontier = paretoFrontier(points);
      marks.push(
        Plot.line(frontier, {
          x: "x",
          y: "y",
          stroke: COLORS.blue,
          strokeWidth: 3,
          curve: "step-after",
        }),
        Plot.dot(frontier, {
          x: "x",
          y: "y",
          r: 7,
          fill: COLORS.paper,
          stroke: COLORS.blue,
          strokeWidth: 3,
        }),
      );
    }

    marks.push(
      Plot.dot(points, {
        x: "x",
        y: "y",
        r: (point) => point.group === "default" ? 4.5 : 7,
        fill: "color",
        fillOpacity: (point) => point.group === "default" ? 0.5 : 1,
        stroke: (point) => point.group === "default" ? COLORS.paper : COLORS.ink,
        strokeWidth: (point) => point.group === "default" ? 0.8 : 1.5,
        symbol: "symbol",
        channels: {
          configuration: { value: "label", label: "Configuration" },
          coverage: { value: (point) => formatX(point.x), label: figure.dataset.tooltipX },
          recovered: { value: (point) => `${point.y}${ySuffix}`, label: figure.dataset.tooltipY },
          residual: {
            value: (point) => `${point.residual >= 0 ? "+" : ""}${point.residual.toFixed(1)}`,
            label: figure.dataset.tooltipResidual,
          },
          ratio: {
            value: (point) => point.y > 0 ? currency.format(point.x / point.y) : "—",
            label: figure.dataset.tooltipRatio,
          },
          attempts: { value: "attempts", label: figure.dataset.tooltipAttempts },
        },
        tip: {
          format: {
            x: false,
            y: false,
            fill: false,
            fillOpacity: false,
            stroke: false,
            strokeWidth: false,
            symbol: false,
            r: false,
            residual: figure.dataset.regression === "linear",
            ratio: Boolean(figure.dataset.tooltipRatio),
            attempts: Boolean(figure.dataset.tooltipAttempts),
          },
        },
      }),
    );

    if (!compact) {
      marks.push(
        Plot.text(primaryPoint, { x: "x", y: "y", text: "label", dy: -15, fontWeight: 800, fill: COLORS.blue }),
        Plot.text(secondaryPoint, { x: "x", y: "y", text: "label", dx: -12, dy: 14, textAnchor: "end", fontWeight: 800, fill: COLORS.coral }),
        Plot.text(referencePoint, { x: "x", y: "y", text: "label", dx: -12, dy: -12, textAnchor: "end", fontWeight: 800, fill: COLORS.ink }),
      );
    }

    const chart = Plot.plot({
      width,
      height: compact ? 390 : 510,
      marginTop: 28,
      marginRight: compact ? 18 : 44,
      marginBottom: compact ? 82 : 68,
      marginLeft: compact ? 58 : 72,
      x: {
        domain: [number(figure.dataset.xMin), number(figure.dataset.xMax)],
        type: figure.dataset.xScale,
        label: figure.dataset.xLabel,
        grid: true,
        nice: false,
        tickFormat: figure.dataset.xFormat === "currency"
          ? (value) => `$${Number(value).toLocaleString(document.documentElement.lang || "en", { maximumFractionDigits: 0 })}`
          : undefined,
      },
      y: {
        domain: [number(figure.dataset.yMin), number(figure.dataset.yMax)],
        label: figure.dataset.yLabel,
        grid: true,
        nice: false,
        ticks: Math.max(2, number(figure.dataset.yMax) - number(figure.dataset.yMin)),
      },
      marks,
    });
    chart.querySelectorAll("style").forEach((style) => style.remove());
    chart.setAttribute("role", "img");
    chart.setAttribute("aria-labelledby", `${target.id}-title`);
    chart.setAttribute("aria-describedby", `${target.id}-description`);
    target.replaceChildren(chart);
    figure.classList.add("is-enhanced");
  };

  document.querySelectorAll("[data-scatter-chart]").forEach((figure) => {
    let frame;
    const refresh = () => {
      window.cancelAnimationFrame(frame);
      frame = window.requestAnimationFrame(() => render(figure));
    };
    refresh();
    new ResizeObserver(refresh).observe(figure.querySelector(".article-scatter-chart__plot"));
  });
})();
