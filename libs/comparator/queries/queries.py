PRODUCTS_MATCHED = """
    SELECT 
        p.IDProducto,
        p.Codebar AS ean,
        CONCAT(p.Producto, ' ', p.Presentacion) AS descripcion,
        l.Nombre AS Proveedor,
        p.IDLaboratorio,
        p.Activo
    FROM 
        productos AS p
    INNER JOIN 
        laboratorios AS l
    ON 
        p.IDLaboratorio = l.IDLaboratorio
    WHERE 
        p.IDProducto IN %(id_producto_array)s;
"""

ALL_CODEBARS = """
    SELECT 
        productos.IDProducto AS IDProducto, 
        productos.Codebar AS Codebar,
        'S' AS EsCodigoPrincipal
    FROM 
        productos;

    UNION ALL

    SELECT 
        productoscodebars.IDProducto AS IDProducto, 
        productoscodebars.codebar AS Codebar,
        'N' AS EsCodigoPrincipal
    FROM 
        productoscodebars;

"""
