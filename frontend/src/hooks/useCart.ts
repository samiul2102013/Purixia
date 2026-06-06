import { useCartStore } from '../stores/cartStore';

export function useCart() {
  const items = useCartStore((state) => state.items);
  const count = useCartStore((state) => state.count);
  const grandTotal = useCartStore((state) => state.grandTotal);
  const loading = useCartStore((state) => state.loading);
  const isDrawerOpen = useCartStore((state) => state.isDrawerOpen);

  const fetchCart = useCartStore((state) => state.fetchCart);
  const addItem = useCartStore((state) => state.addItem);
  const updateItem = useCartStore((state) => state.updateItem);
  const removeItem = useCartStore((state) => state.removeItem);
  const clearCart = useCartStore((state) => state.clearCart);
  
  const openDrawer = useCartStore((state) => state.openDrawer);
  const closeDrawer = useCartStore((state) => state.closeDrawer);
  const toggleDrawer = useCartStore((state) => state.toggleDrawer);

  return {
    items,
    count,
    grandTotal,
    loading,
    isDrawerOpen,
    fetchCart,
    addItem,
    updateItem,
    removeItem,
    clearCart,
    openDrawer,
    closeDrawer,
    toggleDrawer,
  };
}
