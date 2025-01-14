PRODUCTS_MATCHED = """
    SELECT 
        p.IDProducto,
        p.Codebar AS ean,
        CONCAT(p.Producto, ' ', p.Presentacion) AS descripcion,
        pr.Nombre AS Proveedor,
        pr.IDProveedor AS IDProveedor,
        l.Nombre AS Laboratorio,
        p.IDLaboratorio,
        p.Costo,
        CASE 
            WHEN p.idTipoIVA = 2 THEN 10.5
            WHEN p.idTipoIVA = 3 THEN 21
            WHEN p.idTipoIVA = 4 THEN 27
            ELSE 0
        END AS iva,
        p.Costo + (p.Costo * CASE 
            WHEN p.idTipoIVA = 2 THEN 0.105
            WHEN p.idTipoIVA = 3 THEN 0.21
            WHEN p.idTipoIVA = 4 THEN 0.27
            ELSE 0
        END) AS precio_iva,
        p.MargenPVP AS margen_pvp,
        ROUND((p.Costo + (p.Costo * CASE 
            WHEN p.idTipoIVA = 2 THEN 0.105
            WHEN p.idTipoIVA = 3 THEN 0.21
            WHEN p.idTipoIVA = 4 THEN 0.27
            ELSE 0
        END)) * (1 + p.MargenPVP / 100), 2) AS pvp,
        p.Activo
    FROM 
        productos AS p
    INNER JOIN 
        laboratorios AS l ON p.IDLaboratorio = l.IDLaboratorio
    INNER JOIN 
        proveedores AS pr ON p.IDProveedor = pr.IDProveedor
    WHERE  
        p.IDProducto IN %(id_producto_array)s;

"""

PRODUCTS_BY_PROVIDER = """
    SELECT 
        p.IDProducto,
        p.Codebar AS ean,
        CONCAT(p.Producto, ' ', p.Presentacion) AS descripcion,
        pr.Nombre AS Proveedor,
        pr.IDProveedor AS IDProveedor,
        l.Nombre AS Laboratorio,
        p.IDLaboratorio,
        p.Activo
    FROM 
        productos AS p
    INNER JOIN 
        laboratorios AS l
        ON p.IDLaboratorio = l.IDLaboratorio
    INNER JOIN 
        proveedores AS pr
        ON p.IDProveedor = pr.IDProveedor
    WHERE 
        pr.IDProveedor = %(id_provider)s;
"""

ALL_CODEBARS = """
    SELECT 
        p.IDProducto AS IDProducto, 
        p.Codebar AS Codebar,
        'S' AS EsCodigoPrincipal
    FROM 
        productos AS p

    UNION ALL

    SELECT 
        pc.IDProducto AS IDProducto, 
        pc.Codebar AS Codebar,
        'N' AS EsCodigoPrincipal
    FROM 
        productoscodebars AS pc;
"""

ALL_PROVIDERS = """
    SELECT
        IDProveedor,
        Nombre
    FROM
        proveedores;
"""