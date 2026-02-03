# Red Wing Shoes order confirmations to csv

1. Read order confirmation (pypdf)
2. Identify meta data (Order no., Order dt., Your PO#))
3. Identify first row (Each row contains 3 rows)
```
96356 SML PR5 24.00 120.00
INSOLE, LEATHER W/FOAM
Available
03590 H 110 PR1 188.00 188.00

Available
```
4. Transform each row to csv
