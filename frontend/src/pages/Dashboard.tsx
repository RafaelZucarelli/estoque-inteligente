import { useEffect, useState } from "react";
import { getDashboard } from "../services/productService";
import type { ProductWithForecast } from "../types/Product";

const statusColors: Record<string, string> = {
  ok: "#4caf50",
  atencao: "#ff9800",
  critico: "#f44336",
  sem_dados: "#9e9e9e",
};

const statusLabels: Record<string, string> = {
  ok: "OK",
  atencao: "Atenção",
  critico: "Crítico",
  sem_dados: "Sem dados",
};

function Dashboard() {
  const [products, setProducts] = useState<ProductWithForecast[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadDashboard() {
      try {
        const data = await getDashboard();
        setProducts(data);
      } catch (err) {
        setError("Não foi possível carregar os produtos.");
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, []);

  if (loading) return <p>Carregando produtos...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div>
      <h1>Dashboard de Estoque</h1>
      <table>
        <thead>
          <tr>
            <th>Status</th>
            <th>Nome</th>
            <th>SKU</th>
            <th>Estoque Atual</th>
            <th>Média de Vendas/dia</th>
            <th>Dias até Zerar</th>
          </tr>
        </thead>
        <tbody>
          {products.map((product) => (
            <tr key={product.id}>
              <td>
                <span
                  style={{
                    display: "inline-block",
                    width: 12,
                    height: 12,
                    borderRadius: "50%",
                    backgroundColor: statusColors[product.status],
                    marginRight: 8,
                  }}
                ></span>
                {statusLabels[product.status]}
              </td>
              <td>{product.name}</td>
              <td>{product.sku}</td>
              <td>{product.current_stock}</td>
              <td>{product.average_daily_sales}</td>
              <td>
                {product.days_until_stockout !== null
                  ? `${product.days_until_stockout} dias`
                  : "-"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Dashboard;
