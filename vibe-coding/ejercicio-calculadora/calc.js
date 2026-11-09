// Lógica de la calculadora de hipoteca, sin dependencias del navegador.
// En el navegador queda como `window.Hipoteca`; en Node se importa con require.
(function (root) {
  "use strict";

  const RULES = {
    amount: { label: "El importe", max: 1e9, allowZero: false },
    rate:   { label: "El tipo de interés", max: 100, allowZero: true },
    years:  { label: "El plazo", max: 50, allowZero: false },
  };

  const totalMonths = years => Math.round(years * 12);

  // Valida un campo a partir del texto escrito.
  // Devuelve { value, error }: value es null si hay error.
  function parseField(id, raw) {
    const rule = RULES[id];
    const text = String(raw == null ? "" : raw).trim();
    const v = Number(text);
    let error = "";
    if (text === "" || !Number.isFinite(v)) error = "Introduce un número.";
    else if (v < 0) error = rule.label + " no puede ser negativo.";
    else if (v === 0 && !rule.allowZero) error = rule.label + " debe ser mayor que 0.";
    else if (v > rule.max) error = rule.label + " no puede ser mayor que " + rule.max + ".";
    else if (id === "years" && totalMonths(v) < 1) error = "El plazo debe ser de al menos 1 mes.";
    return error ? { value: null, error } : { value: v, error: "" };
  }

  // Sistema francés: cuota mensual constante.
  function monthlyPayment(principal, annualRate, years) {
    const n = totalMonths(years);
    const r = annualRate / 100 / 12;
    return r === 0
      ? principal / n
      : principal * r / (1 - Math.pow(1 + r, -n));
  }

  // Tabla anual: simula mes a mes con la misma cuota. El último mes amortiza
  // exactamente el saldo restante para que el pendiente final sea 0.
  function schedule(principal, annualRate, years, monthly) {
    const n = totalMonths(years);
    const r = annualRate / 100 / 12;
    const rows = [];
    let balance = principal;
    for (let m = 1; m <= n; m++) {
      const interest = balance * r;
      const capital = m === n ? balance : monthly - interest;
      balance = m === n ? 0 : balance - capital;
      const y = Math.ceil(m / 12);
      if (!rows[y - 1]) rows[y - 1] = { year: y, interest: 0, capital: 0, balance: 0 };
      const row = rows[y - 1];
      row.interest += interest;
      row.capital += capital;
      row.balance = balance;
    }
    return rows;
  }

  // Todo junto. Total e intereses salen de la misma simulación que la tabla,
  // así las cifras de cabecera y la fila de totales siempre coinciden.
  function summary(principal, annualRate, years) {
    const monthly = monthlyPayment(principal, annualRate, years);
    const rows = schedule(principal, annualRate, years, monthly);
    let interest = 0, capital = 0;
    for (const row of rows) { interest += row.interest; capital += row.capital; }
    return { monthly, rows, interest, capital, total: principal + interest };
  }

  const api = { RULES, parseField, monthlyPayment, schedule, summary };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.Hipoteca = api;
})(typeof window !== "undefined" ? window : globalThis);
