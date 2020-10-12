SELECT TR.client_id,
sum(CASE WHEN PRD_NOM.product_type="MEUBLE" then (TR.prod_price* TR.prod_qty)  END) as ventes_meuble,
sum(CASE WHEN PRD_NOM.product_type="DECO" then (TR.prod_price* TR.prod_qty)  END)as ventes_deco
FROM TRANSACTIONS  TR
LEFT JOIN PRODUCT_NOMENCLATURE PRD_NOM ON TR.prop_id= PRD_NOM.product_id
where TR.date BETWEEN "2019-01-01" and "2019-12-31"
group by client_id