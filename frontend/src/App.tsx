import { Routes, Route, Link } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import ProductForm from "./pages/ProductForm";
import StockMovementForm from "./pages/StockMovementForm";

function App() {
  return (
    <div>
      <nav style={{ display: "flex", gap: "16px", padding: "16px", borderBottom: "1px solid #ccc" }}>
        <Link to="/">Dashboard</Link>
        <Link to="/novo-produto">Cadastrar Produto</Link>
        <Link to="/movimentacao">Registrar Movimentação</Link>
      </nav>

      <div style={{ padding: "16px" }}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/novo-produto" element={<ProductForm />} />
          <Route path="/movimentacao" element={<StockMovementForm />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
