import api from "./api";
import type { Product, ProductWithForecast } from "../types/Product";

export async function getProducts(): Promise<Product[]> {
  const response = await api.get<Product[]>("/products/");
  return response.data;
}

export async function getDashboard(): Promise<ProductWithForecast[]> {
  const response = await api.get<ProductWithForecast[]>("/products/dashboard");
  return response.data;
}

export interface ProductCreatePayload {
  name: string;
  sku: string;
  current_stock: number;
  reorder_point: number;
  unit_cost: number;
}

export async function createProduct(payload: ProductCreatePayload): Promise<Product> {
  const response = await api.post<Product>("/products/", payload);
  return response.data;
}

export async function registerSale(productId: number, quantity: number) {
  const response = await api.post(`/products/${productId}/sale`, { quantity });
  return response.data;
}

export async function registerRestock(productId: number, quantity: number) {
  const response = await api.post(`/products/${productId}/restock`, { quantity });
  return response.data;
}
