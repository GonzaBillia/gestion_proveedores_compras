P_BY_EAN = """
SELECT 
    IDProducto, 
    Troquel, 
    Codebar, 
    Producto, 
    idProveedor
FROM productos
WHERE Codebar IN (%(placeholders)s)
"""
