PORDUCTS_BY_PROVIDER = """
    SELECT 
        ac.IDProducto,
        ac.Codebar AS ean,
        CONCAT(p.Producto, ' ', p.Presentacion) AS descripcion,
        l.Nombre AS Proveedor,
        p.IDLaboratorio
    FROM (
        SELECT productoscodebars.IDProducto AS IDProducto, productoscodebars.codebar AS Codebar
        FROM productoscodebars 
        LEFT JOIN productos
        ON productos.IDProducto = productoscodebars.IDProducto

        UNION ALL

        SELECT productos.IDProducto AS IDProducto, productos.Codebar AS Codebar
        FROM productos
        WHERE productos.Activo = 's'
    ) AS ac
    INNER JOIN productos AS p
        ON ac.IDProducto = p.IDProducto
    INNER JOIN laboratorios AS l
        ON p.IDLaboratorio = l.IDLaboratorio
    WHERE l.IDLaboratorio = %(id_provider)s;
"""


