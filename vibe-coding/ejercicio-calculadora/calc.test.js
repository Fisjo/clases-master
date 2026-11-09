// Ejecutar con: node --test
const test = require("node:test");
const assert = require("node:assert/strict");
const { parseField, monthlyPayment, summary } = require("./calc.js");

const close = (a, b, eps = 0.005) => assert.ok(Math.abs(a - b) < eps, `${a} no está cerca de ${b}`);

test("200.000 € al 3 % a 30 años da 843,21 €/mes", () => {
  close(monthlyPayment(200000, 3, 30), 843.21);
});

test("la suma del capital amortizado es el importe y el pendiente final es 0", () => {
  for (const [p, r, y] of [[200000, 3, 30], [150000, 0, 10], [100000, 5, 2.5], [1000, 4, 0.5], [50000, 7.9, 50]]) {
    const s = summary(p, r, y);
    close(s.capital, p, 1e-6);
    assert.equal(s.rows.at(-1).balance, 0);
  }
});

test("tipo 0 %: cuota = importe / meses y cero intereses", () => {
  const s = summary(120000, 0, 10);
  close(s.monthly, 1000);
  close(s.interest, 0, 1e-6);
  close(s.total, 120000, 1e-6);
});

test("plazo fraccionario: 2,5 años son 3 filas anuales", () => {
  assert.equal(summary(100000, 5, 2.5).rows.length, 3);
});

test("plazo de 1 mes: una fila y todo el capital en ella", () => {
  const s = summary(1000, 4, 1 / 12);
  assert.equal(s.rows.length, 1);
  close(s.rows[0].capital, 1000, 1e-6);
});

test("total e intereses coinciden con la cuota por el número de meses", () => {
  const s = summary(200000, 3, 30);
  close(s.total, s.monthly * 360, 0.01);
  close(s.total - 200000, s.interest, 1e-6);
});

test("los intereses anuales decrecen y el capital crece (sistema francés)", () => {
  const { rows } = summary(200000, 3, 30);
  for (let i = 1; i < rows.length; i++) {
    assert.ok(rows[i].interest < rows[i - 1].interest);
    assert.ok(rows[i].capital > rows[i - 1].capital);
  }
});

test("validación: casos erróneos", () => {
  assert.match(parseField("amount", "").error, /número/);
  assert.match(parseField("amount", "abc").error, /número/);
  assert.match(parseField("amount", "-5").error, /negativo/);
  assert.match(parseField("amount", "0").error, /mayor que 0/);
  assert.match(parseField("years", "51").error, /mayor que 50/);
  assert.match(parseField("years", "0.01").error, /al menos 1 mes/);
  assert.match(parseField("rate", "101").error, /mayor que 100/);
  assert.equal(parseField("years", "100000").value, null);
});

test("validación: casos válidos", () => {
  assert.equal(parseField("rate", "0").value, 0);
  assert.equal(parseField("rate", "3.25").value, 3.25);
  assert.equal(parseField("years", "50").value, 50);
  assert.equal(parseField("years", "0.1").value, 0.1);
});
