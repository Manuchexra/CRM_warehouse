# backend/seeds/seed.py
import sys
from pathlib import Path

# Add parent directory to path so that "app" module can be found
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.user import User, UserRole
from app.models.customer import Customer
from app.models.product import Product
from app.models.order import Order, OrderItem, OrderStatus
from app.models.inventory import Inventory
from app.core.security import get_password_hash
from decimal import Decimal
from datetime import datetime, timedelta
import random

def seed_database():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if already seeded (if any user exists)
        if db.query(User).count() > 0:
            print("Database already has data. Skipping seed.")
            return
        
        print("🌱 Seeding database...")
        
        # 1. Create users
        admin = User(
            full_name="Admin User",
            email="admin@example.com",
            password_hash=get_password_hash("admin123"),
            role=UserRole.ADMIN,
            is_active=True
        )
        warehouse_manager = User(
            full_name="Ali Valiev",
            email="warehouse@example.com",
            password_hash=get_password_hash("warehouse123"),
            role=UserRole.WAREHOUSE_MANAGER,
            is_active=True
        )
        sales_manager = User(
            full_name="Nilufar Karimova",
            email="sales@example.com",
            password_hash=get_password_hash("sales123"),
            role=UserRole.SALES_MANAGER,
            is_active=True
        )
        employee = User(
            full_name="Jasur Rakhimov",
            email="employee@example.com",
            password_hash=get_password_hash("employee123"),
            role=UserRole.EMPLOYEE,
            is_active=True
        )
        db.add_all([admin, warehouse_manager, sales_manager, employee])
        db.commit()
        print(f"✅ Created {db.query(User).count()} users")
        
        # 2. Create customers
        customers_data = [
            {"company_name": "Toshkent Fashion Group", "contact_person": "Alisher Karimov", "phone": "+998901234567", "email": "alisher@toshfashion.uz", "address": "Toshkent, Chilonzor 9", "tax_id": "123456789"},
            {"company_name": "Samarqand Textile", "contact_person": "Zarina Saidova", "phone": "+998902345678", "email": "zarina@samtex.uz", "address": "Samarqand, Registon ko'chasi", "tax_id": "234567890"},
            {"company_name": "Buxoro Silk House", "contact_person": "Rustam Akhmedov", "phone": "+998903456789", "email": "rustam@bukhara.uz", "address": "Buxoro, Xiyobon 15", "tax_id": "345678901"},
            {"company_name": "Andijon Apparel", "contact_person": "Gulnora Tursunova", "phone": "+998904567890", "email": "gulnora@andapp.uz", "address": "Andijon, Navoiy 22", "tax_id": "456789012"},
            {"company_name": "Qashqadaryo Trade", "contact_person": "Bobur Nematov", "phone": "+998905678901", "email": "bobur@qash.uz", "address": "Qarshi, Mustaqillik 5", "tax_id": "567890123"}
        ]
        customers = []
        for c in customers_data:
            cust = Customer(**c)
            db.add(cust)
            customers.append(cust)
        db.commit()
        print(f"✅ Created {len(customers)} customers")
        
        # 3. Create products
        products_data = [
            {"name": "Erkaklar ko'ylagi (M)", "sku": "SHIRT-M-001", "description": "Paxta mato, oq rang", "unit_price": Decimal("85000"), "category": "Erkaklar"},
            {"name": "Erkaklar ko'ylagi (L)", "sku": "SHIRT-L-001", "description": "Paxta mato, oq rang", "unit_price": Decimal("85000"), "category": "Erkaklar"},
            {"name": "Ayollar libosi (S)", "sku": "DRESS-S-002", "description": "Yozgi libos, gul naqsh", "unit_price": Decimal("120000"), "category": "Ayollar"},
            {"name": "Ayollar libosi (M)", "sku": "DRESS-M-002", "description": "Yozgi libos, gul naqsh", "unit_price": Decimal("120000"), "category": "Ayollar"},
            {"name": "Bolalar sviteri", "sku": "KID-SWEATER-003", "description": "Jun aralashmasi, qizil rang", "unit_price": Decimal("65000"), "category": "Bolalar"},
            {"name": "Sport kostyumi (erkak)", "sku": "TRACK-M-004", "description": "Trikotaj, qora", "unit_price": Decimal("180000"), "category": "Sport"},
            {"name": "Shlyapa (ayollar)", "sku": "HAT-W-005", "description": "Somon shlyapa", "unit_price": Decimal("45000"), "category": "Aksessuarlar"},
            {"name": "Ko'zoynak (quyosh)", "sku": "SUNGLASS-006", "description": "Polarized linzalar", "unit_price": Decimal("95000"), "category": "Aksessuarlar"},
            {"name": "Dasturxon (to'plam)", "sku": "TABLECLOTH-007", "description": "Yog'och naqshli", "unit_price": Decimal("75000"), "category": "Uy to'qimasi"},
            {"name": "Shoyi ro'mol", "sku": "SCARF-008", "description": "Tabiiy shoyi", "unit_price": Decimal("110000"), "category": "Ayollar"}
        ]
        products = []
        for p in products_data:
            prod = Product(**p)
            db.add(prod)
            products.append(prod)
        db.commit()
        print(f"✅ Created {len(products)} products")
        
        # 4. Create inventory for products
        for prod in products:
            inv = Inventory(
                product_id=prod.id,
                stock_quantity=Decimal(str(random.randint(10, 200))),
                reserved_quantity=Decimal("0")
            )
            db.add(inv)
        db.commit()
        print(f"✅ Created inventory for {len(products)} products")
        
        # 5. Create orders
        order_statuses = [OrderStatus.PENDING, OrderStatus.CONFIRMED, OrderStatus.PROCESSING, OrderStatus.SHIPPED, OrderStatus.DELIVERED, OrderStatus.CANCELLED]
        orders_created = 0
        for i in range(20):
            customer = random.choice(customers)
            status = random.choice(order_statuses)
            order = Order(
                customer_id=customer.id,
                order_date=datetime.utcnow() - timedelta(days=random.randint(0, 30)),
                status=status,
                notes=f"Buyurtma {i+1} uchun eslatma",
                total_amount=Decimal("0")
            )
            db.add(order)
            db.flush()
            
            total = Decimal("0")
            num_items = random.randint(1, 3)
            used_products = random.sample(products, min(num_items, len(products)))
            for prod in used_products:
                quantity = Decimal(str(random.randint(1, 10)))
                inventory = db.query(Inventory).filter(Inventory.product_id == prod.id).first()
                if inventory and inventory.stock_quantity >= quantity:
                    # Decrease stock
                    inventory.stock_quantity -= quantity
                    if status in [OrderStatus.CONFIRMED, OrderStatus.PROCESSING, OrderStatus.SHIPPED, OrderStatus.DELIVERED]:
                        inventory.reserved_quantity += quantity
                    
                    subtotal = prod.unit_price * quantity
                    total += subtotal
                    
                    item = OrderItem(
                        order_id=order.id,
                        product_id=prod.id,
                        quantity=quantity,
                        unit_price=prod.unit_price,
                        subtotal=subtotal
                    )
                    db.add(item)
                else:
                    continue
            if total > 0:
                order.total_amount = total
                orders_created += 1
            else:
                db.delete(order)
        db.commit()
        print(f"✅ Created {orders_created} orders with items")
        
        print("\n🎉 Seed completed successfully!")
        print(f"   Users: {db.query(User).count()}")
        print(f"   Customers: {db.query(Customer).count()}")
        print(f"   Products: {db.query(Product).count()}")
        print(f"   Orders: {db.query(Order).count()}")
        print(f"   Order Items: {db.query(OrderItem).count()}")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()