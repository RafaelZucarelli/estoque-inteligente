import { useEffect, useState } from "react";
import { getProducts } from "../services/productService";
import type { Product } from "../types/Product";

function Dashboard() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadProducts() {
      try {
        const data = await getProducts();
        setProducts(data);
      } catch (err) {
        setError("Não foi possível carregar os produtos.");
      } finally {
        setLoading(false);
      }
    }

    loadProducts();
  }, []);

  if (loading) return <p>Carregando produtos...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div>
      <h1>Dashboard de Estoque</h1>
      <table>
        <thead>
          <tr>
            <th>Nome</th>
            <th>SKU</th>
            <th>Estoque Atual</th>
            <th>Ponto de Reposição</th>
          </tr>
        </thead>
        <tbody>
          {products.map((product) => (
            <tr key={product.id}>
              <td>{product.name}</td>
              <td>{product.sku}</td>
              <td>{product.current_stock}</td>
              <td>{product.reorder_point}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Dashboard;