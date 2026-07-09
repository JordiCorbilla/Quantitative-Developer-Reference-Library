# Convertible Bond Parity Example

Related chapter: [../25-convertibles-and-equity-linked-notes.md](../25-convertibles-and-equity-linked-notes.md).

Assume:
- stock price: USD 45
- conversion ratio: 20 shares
- bond par: USD 1,000

```python
stock_price = 45.0
conversion_ratio = 20.0
par = 1_000.0

parity = stock_price * conversion_ratio
conversion_price = par / conversion_ratio
```

Parity is USD 900. The conversion price is USD 50. The bond is out of the money for immediate conversion when the stock trades below USD 50.
