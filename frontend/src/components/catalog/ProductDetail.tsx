'use client';

import * as React from 'react';
import Image from 'next/image';
import { useRouter } from 'next/navigation';
import { Minus, Plus, ShoppingCart } from 'lucide-react';
import { Product } from '../../types';
import { cn, formatPrice, getImageUrl } from '../../lib/utils';
import { useCartStore } from '../../stores/cartStore';
import { useAuth } from '../../hooks/useAuth';
import toast from 'react-hot-toast';

interface ProductDetailProps {
  product: Product;
}

export function ProductDetail({ product }: ProductDetailProps) {
  const router = useRouter();
  const { isLoggedIn } = useAuth();
  const addItem = useCartStore((s) => s.addItem);
  const closeDrawer = useCartStore((s) => s.closeDrawer);
  const [quantity, setQuantity] = React.useState(1);
  const [adding, setAdding] = React.useState(false);
  const [selectedImage, setSelectedImage] = React.useState(product.image);

  const allImages = React.useMemo(() => {
    const gallery = product.images?.map(img => img.image) || [];
    if (product.image && !gallery.includes(product.image)) {
      return [product.image, ...gallery];
    }
    return gallery.length > 0 ? gallery : [product.image];
  }, [product.image, product.images]);

  const handleAddToCart = async () => {
    setAdding(true);
    try {
      await addItem(product.id, quantity);
      toast.success('Added to cart!');
    } catch {
      toast.error('Failed to add to cart');
    } finally {
      setAdding(false);
    }
  };

  const handleBuyNow = async () => {
    if (!isLoggedIn) {
      try {
        await addItem(product.id, quantity);
        closeDrawer();
      } catch (e) {
        console.error('Add to cart before redirect failed', e);
      }
      toast('Please sign up first');
      router.push(`/register?redirect=/checkout&add_to_cart=${product.id}`);
      return;
    }
    setAdding(true);
    try {
      await addItem(product.id, quantity);
      closeDrawer();
      router.push('/checkout');
    } catch {
      toast.error('Failed to add to cart');
    } finally {
      setAdding(false);
    }
  };

  return (
    <div className="max-w-[1440px] mx-auto px-4 sm:px-6 md:px-[40px] lg:px-[80px] py-[20px] font-poppins">
      {/* Product Card */}
      <div className="bg-white rounded-[20px] shadow-[0px_4px_30px_rgba(0,0,0,0.03)] p-[24px] mb-[24px] border border-gray-50">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-[30px]">
          {/* Left: Images (5 columns) */}
          <div className="lg:col-span-5 flex flex-col gap-3">
            <div className="relative aspect-square w-full bg-[#F5F5F5] rounded-[15px] overflow-hidden border border-gray-50">
              <Image
                src={getImageUrl(selectedImage)}
                alt={product.name}
                fill
                className="object-contain p-6"
                priority
              />
            </div>
            {/* Thumbnails */}
            <div className="flex gap-2 overflow-x-auto pb-1 scrollbar-hide">
              {allImages.map((img, i) => (
                <div 
                  key={i} 
                  onClick={() => setSelectedImage(img)}
                  className={cn(
                    "relative w-[60px] h-[60px] bg-[#F5F5F5] rounded-[8px] overflow-hidden border transition-all cursor-pointer shrink-0",
                    selectedImage === img ? "border-[#F4B227]" : "border-gray-100 opacity-60 hover:opacity-100"
                  )}
                >
                  <Image
                    src={getImageUrl(img)}
                    alt={`${product.name} view ${i}`}
                    fill
                    className="object-contain p-1"
                  />
                </div>
              ))}
            </div>
          </div>

          {/* Right: Info (7 columns) */}
          <div className="lg:col-span-7 flex flex-col py-1">
            <div className="flex justify-between items-start mb-2">
              <div>
                <h1 className="text-[22px] font-bold text-black mb-1 leading-tight">{product.name}</h1>
              </div>
              <span className="bg-[#ECFDF5] text-[#10B981] text-[9px] font-bold px-2 py-0.5 rounded-[4px] border border-[#D1FAE5] uppercase tracking-wider">
                In Stock
              </span>
            </div>

            {/* Price & Meta */}
            <div className="flex items-baseline gap-3 mb-4">
              <span className="text-[24px] font-bold text-black">৳ {product.price}</span>
              <span className="text-[14px] text-gray-400 line-through">৳ {parseFloat(product.price) * 1.2}</span>
              <span className="text-[12px] text-red-500 font-bold">20% OFF</span>
            </div>

            {/* Description Preview or Short Info */}
            <div className="mb-6">
              <p className="text-[13px] text-[#666666] leading-relaxed line-clamp-3">
                {product.description || "A premium gadget featuring the latest technology and sleek design. Perfect for your daily needs with high-performance components and durable build quality."}
              </p>
            </div>

            {/* Meta Info */}
            <div className="mb-6">
              <div className="space-y-1.5">
                <span className="text-[11px] font-bold text-black uppercase tracking-wider">SKU</span>
                <p className="text-[12px] text-[#666666]">#PRX-992341</p>
              </div>
            </div>

            {/* Quantity & Actions */}
            <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 sm:gap-4 mb-8">
              <div className="flex items-center border border-gray-200 rounded-[8px] h-[44px] bg-gray-50 w-fit">
                <button 
                  onClick={() => setQuantity(Math.max(1, quantity - 1))}
                  className="w-10 h-full flex items-center justify-center text-gray-400 hover:text-black transition-colors"
                >
                  <Minus className="w-3.5 h-3.5" />
                </button>
                <span className="w-10 h-full flex items-center justify-center text-[14px] font-bold border-x border-gray-200">
                  {quantity}
                </span>
                <button 
                  onClick={() => setQuantity(quantity + 1)}
                  className="w-10 h-full flex items-center justify-center text-gray-400 hover:text-black transition-colors"
                >
                  <Plus className="w-3.5 h-3.5" />
                </button>
              </div>
              
              <div className="flex flex-1 gap-3">
                <button
                  onClick={handleAddToCart}
                  disabled={adding}
                  className="flex-1 h-[44px] bg-black text-white text-[13px] font-bold rounded-[8px] hover:bg-gray-800 transition-all shadow-sm flex items-center justify-center gap-2"
                >
                  <ShoppingCart className="w-4 h-4" />
                  Add to Cart
                </button>
                <button
                  onClick={handleBuyNow}
                  disabled={adding}
                  className="flex-1 h-[44px] bg-[#F4B227] text-white text-[13px] font-bold rounded-[8px] hover:bg-[#D89500] transition-all shadow-sm uppercase tracking-wider"
                >
                  Buy Now
                </button>
              </div>
            </div>

            {/* Description section */}
            <div className="border-t border-gray-100 pt-4">
              <h3 className="text-[13px] font-bold uppercase tracking-wider text-black mb-3">
                Description
              </h3>
              <div className="text-[12px] text-[#666666] leading-relaxed">
                <p className="">{product.description || "A premium high-performance gadget designed for modern lifestyle. Features advanced circuitry, ergonomic design, and industry-leading battery life. Built with sustainable materials without compromising on durability or aesthetic appeal."}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
