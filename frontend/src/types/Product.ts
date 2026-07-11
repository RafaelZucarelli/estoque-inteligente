export interface Product {
  id: number;
  name: string;
  sku: string;
  current_stock: number;
  reorder_point: number;
  unit_cost: number;
}

export interface ProductWithForecast {
  id: number;
  name: string;
  sku: string;
  current_stock: number;
  reorder_point: number;
  unit_cost: number;
  average_daily_sales: number;
  days_until_stockout: number | null;
  status: "ok" | "atencao" | "critico" | "sem_dados";
}
