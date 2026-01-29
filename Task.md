# N+1 проблем (REST vs GraphQL) и JSON vs gRPC (Protobuf)

## 1) N+1 (REST vs GraphQL)

### Колко DB заявки прави `/bookings/{booking_id}` в момента?

Endpoint-ът изпълнява **точно 1 заявка към базата данни**.

- Route-ът извиква:
  ```python
  repo.get_booking_for_rider(...)
  ```
- Repository-то изпълнява:
  ```python
  select(Booking).where(Booking.id == booking_id)
  ```

➡ **1 DB заявка**

В кода **няма отделни repository извиквания** за `driver` или `vehicle`.

---

### Откъде идват `driver name` и `license plate` за *Trip Summary*?

В момента **не се извличат изрично**. Възможни са само два варианта:

1. **Денормализирани данни**  
   Ако `driver_name` и `vehicle_plate` са колони в таблицата `Booking`  
   ➜ отново **1 DB заявка**

2. **Lazy-loaded relationships**  
   Ако `BookingOut` съдържа вложени обекти (`driver`, `vehicle`) и моделът `Booking`
   има lazy relationships:
   - +1 заявка за `booking.driver`
   - +1 заявка за `booking.vehicle`

   ➜ **общо 3 заявки (1 + 2)**

**Извод:**  
По repo и route кода endpoint-ът използва **1 заявка**, освен ако сериализацията
не предизвика lazy loading.

---

### Как скалира при 20 минали резервации?

При list endpoint, реализиран по наивен ORM начин:

- 1 заявка → взимане на 20 bookings
- +20 заявки → drivers
- +20 заявки → vehicles

➡ **41 DB заявки (1 + 2N)**  
Това е класическият **N+1 проблем**.

---

### Как изглежда решението с GraphQL?

#### Network chattiness
Клиентът изпраща **една GraphQL заявка**, която иска точно:
- `booking.status`
- `driver.name`
- `vehicle.licensePlate`

➡ **1 HTTP request**, вместо няколко REST повиквания.

#### DB chattiness
GraphQL **не решава автоматично N+1**.

- При наивни resolvers:
  - 1 заявка за bookings
  - +N заявки за drivers
  - +N заявки за vehicles

- При batching (`DataLoader`, `selectinload`, `joinedload`):
  ➜ **~1–3 DB заявки общо**

---

## 2) JSON vs gRPC (Protobuf) — Live Driver Tracking (1 Hz)

### Защо gRPC / Protobuf е *binary*?

- **JSON** е текстов формат:
  ```json
  { "lat": 42.123, "lon": 23.456 }
  ```
  Съдържа текстови ключове и символи.

- **Protobuf** използва бинарна сериализация:
  - Полетата са номерирани (numeric tags)
  - Стойностите са бинарно кодирани
  - Няма повтарящи се текстови ключове

---

### Типичен размер на payload (GPS update)

Полетата са:
```
driver_id + latitude + longitude + timestamp
```

- **JSON:** ~80–150 bytes
- **Protobuf:** ~20–50 bytes

Размерът зависи от схемата, но **Protobuf почти винаги е значително по-компактен**
за малки телеметрични съобщения.

---

### Защо това е важно при слаб 3G и 1 update/сек?

При 1 Hz GPS updates:

- по-малък payload → по-малко време „в ефир“ → **по-нисък разход на батерия**
- по-малко байтове → по-малко retransmissions → **по-стабилна връзка**
- по-малко трафик → **по-ниска латентност**
- резултат → **по-гладко live tracking**

---

## Обобщение

- REST + ORM без eager loading → висок риск от **N+1**
- GraphQL намалява network chattiness, но **изисква batching**, за да няма N+1
- gRPC + Protobuf е по-подходящ за **чести, реално-времеви мобилни данни**
