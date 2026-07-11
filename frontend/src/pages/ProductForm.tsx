import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createProduct } from "../services/productService";

function ProductForm() {
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [sku, setSku] = useState("");
  const [currentStock, setCurrentStock] = useState(0);
  const [reorderPoint, setReorderPoint] = useState(5);
  const [unitCost, setUnitCost] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setSubmitting(true);

    try {
      await createProduct({
        name,
        sku,
        current_stock: currentStock,
        reorder_point: reorderPoint,
        unit_cost: unitCost,
      });
      navigate("/");
    } catch (err: any) {
      const message = err.response?.data?.detail || "Erro ao criar produto.";
      setError(message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div>
      <h1>Cadastrar Produto</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Nome</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>

        <div>
          <label>SKU</label>
          <input
            type="text"
            value={sku}
            onChange={(e) => setSku(e.target.value)}
            required
          />
        </div>

        <div>
          <label>Estoque inicial</label>
          <input
            type="number"
            value={currentStock}
            onChange={(e) => setCurrentStock(Number(e.target.value))}
            min={0}
          />
        </div>

        <div>
          <label>Ponto de reposição</label>
          <input
            type="number"
            value={reorderPoint}
            onChange={(e) => setReorderPoint(Number(e.target.value))}
            min={0}
          />
        </div>

        <div>
          <label>Custo unitário</label>
          <input
            type="number"
            step="0.01"
            value={unitCost}
            onChange={(e) => setUnitCost(Number(e.target.value))}
            min={0}
          />
        </div>

        {error && <p style={{ color: "red" }}>{error}</p>}

        <button type="submit" disabled={submitting}>
          {submitting ? "Salvando..." : "Salvar"}
        </button>
      </form>
    </div>
  );
}

export default ProductForm;
