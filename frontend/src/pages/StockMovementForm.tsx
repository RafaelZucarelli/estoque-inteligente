import { useEffect, useState } from "react";
import { getProducts, registerSale, registerRestock } from "../services/productService";
import type { Product } from "../types/Product";

function StockMovementForm() {
  const [products, setProducts] = useState<Product[]>([]);
  const [selectedProductId, setSelectedProductId] = useState<number | "">("");
  const [quantity, setQuantity] = useState(1);
  const [movementType, setMovementType] = useState<"sale" | "restock">("sale");
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    getProducts().then(setProducts);
  }, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setMessage(null);

    if (selectedProductId === "") {
      setError("Selecione um produto.");
      return;
    }

    setSubmitting(true);
    try {
      if (movementType === "sale") {
        await registerSale(selectedProductId, quantity);
        setMessage("Venda registrada com sucesso!");
      } else {
        await registerRestock(selectedProductId, quantity);
        setMessage("Reposição registrada com sucesso!");
      }
      setQuantity(1);
    } catch (err: any) {
      const detail = err.response?.data?.detail || "Erro ao registrar movimentação.";
      setError(detail);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div>
      <h1>Registrar Movimentação</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Tipo</label>
          <select
            value={movementType}
            onChange={(e) => setMovementType(e.target.value as "sale" | "restock")}
          >
            <option value="sale">Venda</option>
            <option value="restock">Reposição</option>
          </select>
        </div>

        <div>
          <label>Produto</label>
          <select
            value={selectedProductId}
            onChange={(e) => setSelectedProductId(Number(e.target.value))}
          >
            <option value="">Selecione...</option>
            {products.map((product) => (
              <option key={product.id} value={product.id}>
                {product.name} (estoque: {product.current_stock})
              </option>
            ))}
          </select>
        </div>

        <div>
          <label>Quantidade</label>
          <input
            type="number"
            value={quantity}
            onChange={(e) => setQuantity(Number(e.target.value))}
            min={1}
          />
        </div>

        {error && <p style={{ color: "red" }}>{error}</p>}
        {message && <p style={{ color: "green" }}>{message}</p>}

        <button type="submit" disabled={submitting}>
          {submitting ? "Enviando..." : "Confirmar"}
        </button>
      </form>
    </div>
  );
}

export default StockMovementForm;

