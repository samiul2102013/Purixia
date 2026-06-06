export interface User {
  id: number;
  username: string;
  email: string;
  phone: string;
}

export interface Tokens {
  access: string;
  refresh: string;
}

export interface AuthResponse {
  user: User;
  tokens: Tokens;
}

export interface Category {
  id: number;
  name: string;
  slug: string;
}

export interface CategoryDetail extends Category {
  products: Product[];
}

export interface ProductImage {
  id: number;
  image: string;
}

export interface Product {
  id: number;
  category: number;
  name: string;
  title: string;
  description: string;
  price: string;
  quantity: number;
  rating: string;
  in_stock: boolean;
  image: string | null;
  images: ProductImage[];
  created_at: string;
  updated_at: string;
}

export interface CartProduct {
  id: number;
  name: string;
  price: string;
  image: string | null;
}

export interface CartItem {
  product: CartProduct;
  quantity: number;
  price: string;
  total_price: string;
}

export interface CartResponse {
  items: CartItem[];
  grand_total: string;
  count: number;
}

export interface ShippingInfo {
  name: string;
  email: string;
  phone: string;
  address: string;
}

export type DeliveryType = 'inside' | 'outside';
export type PaymentMethod = 'cod' | 'card' | 'bkash' | 'nagad';
export type OrderStatus = 'pending' | 'confirmed' | 'shipped' | 'delivered' | 'cancelled';

export interface OrderItem {
  id: number;
  product: number;
  product_name: string;
  quantity: number;
  unit_price: string;
  subtotal: string;
}

export interface Order {
  id: number;
  user: number;
  shipping_info: ShippingInfo;
  delivery_type: DeliveryType;
  payment_method: PaymentMethod;
  status: OrderStatus;
  total_amount: string;
  items: OrderItem[];
  created_at: string;
}

export interface PlaceOrderPayload {
  shipping_info: ShippingInfo;
  delivery_type: DeliveryType;
  payment_method: PaymentMethod;
}

export interface Banner {
  id: number;
  title: string;
  subtitle: string;
  image: string;
  is_active: boolean;
  order: number;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface ApiError {
  detail?: string;
  error?: string;
  non_field_errors?: string[];
  [key: string]: string | string[] | undefined;
}
