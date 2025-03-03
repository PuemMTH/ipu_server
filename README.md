# คู่มือการใช้งาน Docker และ Docker Compose สำหรับ IPU Server

---

# 🐳 DOCKER COMMANDS (คำสั่ง Docker พื้นฐาน)

## 🔧 ข้อกำหนดเบื้องต้น

- ติดตั้ง Docker บนเครื่องของคุณ ([ดาวน์โหลด Docker](https://www.docker.com/get-started))

## 🔨 การสร้าง Docker Image

1. เปิด Terminal หรือ Command Prompt
2. นำทางไปยังไดเรกทอรีของโปรเจค
   ```bash
   cd /path/to/ipu_server
   ```
3. สร้าง Docker image
   ```bash
   docker build -t ipu-server .
   ```

## 🚀 การรัน Container

```bash
docker run -p 8080:80 -d --name ipu-container ipu-server
```

**คำอธิบาย:**
- `-p 8080:80`: Port forwarding จาก port 8080 บนเครื่อง host ไปยัง port 80 ของ container
- `-d`: รัน container ในโหมด detached (background)
- `--name ipu-container`: กำหนดชื่อให้กับ container
- `ipu-server`: ชื่อของ image ที่จะใช้

## 📝 คำสั่ง Docker พื้นฐานที่จำเป็นต้องรู้

### 1️⃣ docker run - รัน Container
- **คำอธิบาย**: ใช้เพื่อรัน container ใหม่จาก image ที่ระบุ
- **รูปแบบพื้นฐาน**: `docker run [OPTIONS] IMAGE [COMMAND] [ARG...]`
- **ตัวอย่าง**: `docker run -d -p 8080:80 nginx`
- **ตัวเลือกที่ใช้บ่อย**:
  - `-d`: รันแบบ detached (ใน background)
  - `-p 8080:80`: map พอร์ต 8080 (host) ไปที่พอร์ต 80 (container)
  - `-v /host/path:/container/path`: mount volume
  - `-e KEY=VALUE`: กำหนดค่า environment variable
  - `--name my-container`: กำหนดชื่อให้ container
  - `-it`: เปิด interactive terminal (ใช้เมื่อต้องการเข้าใช้งาน shell)
  - `--rm`: ลบ container อัตโนมัติเมื่อหยุดทำงาน

### 2️⃣ docker ps - ดูรายการ Container
- **คำอธิบาย**: แสดงรายการ container ที่กำลังรันอยู่
- **รูปแบบพื้นฐาน**: `docker ps [OPTIONS]`
- **ตัวอย่าง**:
  - `docker ps`: แสดงเฉพาะ container ที่กำลังทำงาน
  - `docker ps -a`: แสดง container ทั้งหมด (รวมที่หยุดแล้ว)
  - `docker ps -q`: แสดงเฉพาะ container ID (ใช้กับคำสั่งอื่นๆ)
  - `docker ps -s`: แสดงขนาดของ container
  - `docker ps --filter "status=exited"`: กรองเฉพาะ container ที่หยุดแล้ว
  - `docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Status}}"`: แสดงในรูปแบบตารางกำหนดเอง

### 3️⃣ docker exec - รันคำสั่งใน Container
- **คำอธิบาย**: รันคำสั่งใน container ที่กำลังรันอยู่
- **รูปแบบพื้นฐาน**: `docker exec [OPTIONS] CONTAINER COMMAND [ARG...]`
- **ตัวอย่าง**:
  - `docker exec my-container ls -la`: รันคำสั่ง ls -la ใน container
  - `docker exec -it my-container bash`: เข้า bash shell แบบ interactive
  - `docker exec -it my-container sh`: เข้า sh shell (สำหรับ alpine image)
  - `docker exec -e VAR=value my-container command`: รันคำสั่งพร้อมกำหนดค่า env

**การใช้ -it (interactive + tty)**:
- `-i` หรือ `--interactive`: คงการเชื่อมต่อ STDIN เปิดไว้
- `-t` หรือ `--tty`: จัดสรร pseudo-TTY terminal
- **ความสำคัญ**: ช่วยให้สามารถโต้ตอบกับ shell ได้ (เช่น รับ input, แสดง prompt, ใช้ arrow keys)
- **ตัวอย่างการใช้งาน**:
  ```bash
  # เข้าใช้งาน shell แบบเต็มรูปแบบ
  docker exec -it web-container bash
  
  # รันคำสั่งแบบโต้ตอบ
  docker exec -it db-container mysql -u root -p
  
  # ดูไฟล์แบบโต้ตอบ (กด space เพื่อเลื่อนหน้า)
  docker exec -it app-container less /var/log/app.log
  ```

### 4️⃣ docker pull - ดึง Image
- **คำอธิบาย**: ดึง image จาก registry (เช่น Docker Hub)
- **รูปแบบพื้นฐาน**: `docker pull [OPTIONS] NAME[:TAG|@DIGEST]`
- **ตัวอย่าง**:
  - `docker pull ubuntu:latest`: ดึง Ubuntu เวอร์ชันล่าสุด
  - `docker pull nginx:1.21-alpine`: ดึง Nginx เวอร์ชัน 1.21 บน Alpine
  - `docker pull --platform linux/amd64 mysql`: ระบุแพลตฟอร์มเฉพาะ

### 5️⃣ docker image - จัดการ Image
- **คำอธิบาย**: จัดการ image เช่น ดูรายการหรือลบ
- **รูปแบบพื้นฐาน สำหรับดูรายการ**: `docker image ls [OPTIONS]`
- **ตัวอย่าง**:
  - `docker image ls`: แสดงรายการ images ทั้งหมด
  - `docker image ls -q`: แสดงเฉพาะ ID (ใช้กับคำสั่งอื่นๆ)
  - `docker image rm [IMAGE_ID]`: ลบ image ตาม ID
  - `docker image prune`: ลบ images ที่ไม่ได้ใช้งาน (dangling)
  - `docker image prune -a`: ลบ images ที่ไม่ได้ใช้งานทั้งหมด (ระวัง!)
- **หมายเหตุ**: 
  - สามารถใช้ `docker rmi [image_id]` เพื่อลบ image ได้ 
  - หลีกเลี่ยงการใช้ `docker image prune` หากไม่แน่ใจ เพราะอาจลบ image ที่จำเป็นโดยไม่ได้ตั้งใจ

### 6️⃣ docker stop/start/restart - ควบคุมสถานะ Container
- **คำอธิบาย**: หยุด/เริ่ม/รีสตาร์ท container
- **รูปแบบพื้นฐาน**: `docker [stop|start|restart] [OPTIONS] CONTAINER [CONTAINER...]`
- **ตัวอย่าง**:
  - `docker stop my-container`: หยุดการทำงานของ container
  - `docker start my-container`: เริ่มการทำงานของ container ที่หยุดอยู่
  - `docker restart my-container`: รีสตาร์ท container
  - `docker stop $(docker ps -q)`: หยุด container ทั้งหมดที่กำลังทำงาน

### 7️⃣ docker logs - ดู Logs ของ Container
- **คำอธิบาย**: ดู logs ที่ถูกส่งออกมาจาก container
- **รูปแบบพื้นฐาน**: `docker logs [OPTIONS] CONTAINER`
- **ตัวอย่าง**:
  - `docker logs my-container`: แสดง logs ทั้งหมด
  - `docker logs -f my-container`: แสดง logs แบบ follow (แสดงต่อเนื่อง)
  - `docker logs --tail 100 my-container`: แสดง 100 บรรทัดล่าสุด
  - `docker logs --since 2023-01-01 my-container`: แสดง logs ตั้งแต่วันที่กำหนด
  - `docker logs -f --until=2m my-container`: follow logs จนถึง 2 นาทีที่ผ่านมา

### 8️⃣ docker rm - ลบ Container
- **คำอธิบาย**: ลบ container ที่ไม่ได้ใช้งาน
- **รูปแบบพื้นฐาน**: `docker rm [OPTIONS] CONTAINER [CONTAINER...]`
- **ตัวอย่าง**:
  - `docker rm my-container`: ลบ container ชื่อ my-container
  - `docker rm -f my-container`: บังคับลบ container ที่กำลังทำงานอยู่
  - `docker rm $(docker ps -aq -f status=exited)`: ลบ container ที่หยุดทำงานทั้งหมด

### 9️⃣ docker cp - คัดลอกไฟล์ระหว่าง Container และ Host
- **คำอธิบาย**: คัดลอกไฟล์/โฟลเดอร์ระหว่าง container และระบบ host
- **รูปแบบพื้นฐาน**: `docker cp [OPTIONS] CONTAINER:SRC_PATH DEST_PATH|-`
- **ตัวอย่าง**:
  - `docker cp my-container:/app/log.txt ./logs/`: คัดลอกไฟล์จาก container มาที่ host
  - `docker cp ./config.json my-container:/app/`: คัดลอกไฟล์จาก host ไปที่ container

## 🌐 การเข้าถึง Application

หลังจากรัน container เสร็จเรียบร้อย คุณสามารถเข้าถึง application ได้ที่:

```
http://localhost:8080
```

---

# 🔄 DOCKER COMPOSE COMMANDS (คำสั่ง Docker Compose)

## 📊 เปรียบเทียบคำสั่ง Docker Compose

| คำสั่ง | Build Image? | รัน Container? | โหมดการรัน | เหมาะกับกรณีใด |
|-------|-------------|--------------|-----------|--------------|
| docker-compose up | ถ้ายังไม่มี/เปลี่ยน | ใช่ | Foreground | รันและดู log เพื่อ debug |
| docker-compose up -d | ถ้ายังไม่มี/เปลี่ยน | ใช่ | Background | รันในพื้นหลัง ไม่ดู log |
| docker-compose up --build | ใช่ (บังคับ build) | ใช่ | Foreground | อัพเดท image แล้วรันพร้อมดู log |

## 📚 คำสั่ง Docker Compose ที่สำคัญ

### 1️⃣ docker-compose up
- **คำอธิบาย**: รัน service ทั้งหมดที่กำหนดในไฟล์ docker-compose.yml ในโหมด foreground
- **การใช้งาน**: เหมาะสำหรับการดู log แบบเรียลไทม์เพื่อ debug
- **ข้อควรระวัง**: จะไม่บังคับ rebuild image ใหม่ถ้ามีอยู่แล้ว ซึ่งอาจไม่สะท้อนการเปลี่ยนแปลงโค้ดล่าสุด

### 2️⃣ docker-compose up -d
- **คำอธิบาย**: รัน service ทั้งหมดที่กำหนดในไฟล์ docker-compose.yml ในโหมด detached (background)
- **การใช้งาน**: เหมาะสำหรับการรันแอพพลิเคชันในสภาพแวดล้อมจริง

### 3️⃣ docker-compose up --build
- **คำอธิบาย**: รัน service ทั้งหมดใน docker-compose.yml พร้อมบังคับ build image ใหม่ก่อนรัน
- **การใช้งาน**: เหมาะสำหรับเมื่อมีการเปลี่ยนแปลงโค้ดและต้องการอัพเดท image
- **ข้อดี**: มั่นใจได้ว่าจะใช้โค้ดล่าสุดเสมอ แม้จะใช้เวลามากกว่า

### 4️⃣ docker-compose build
- **คำอธิบาย**: คำสั่งนี้ใช้เฉพาะการ build image ตามที่กำหนดใน docker-compose.yml เท่านั้น
- **ข้อสำคัญ**: ไม่มีการรัน container หลังจาก build เสร็จ
- **การใช้งาน**: เหมาะสำหรับเมื่อต้องการเตรียม image ไว้ล่วงหน้า แต่ยังไม่ต้องการรัน container
- **รูปแบบ**: `docker-compose build [service_name]` (ถ้าไม่ระบุ service_name จะ build ทั้งหมด)

### 5️⃣ docker-compose down
- **คำอธิบาย**: หยุดและลบ container, network ที่สร้างจาก docker-compose.yml
- **การใช้งาน**: ใช้ตอนต้องการหยุดโปรเจคทั้งหมดและล้าง container ทิ้ง (แต่ image ยังอยู่)

### 6️⃣ docker-compose stop
- **คำอธิบาย**: หยุด container แต่ไม่ลบ
- **การใช้งาน**: เหมาะสำหรับเมื่อต้องการหยุดชั่วคราวแต่จะกลับมารันใหม่ภายหลัง

## 🔄 ความแตกต่างที่สำคัญระหว่างคำสั่ง Build ใน Docker Compose

### 📋 ตารางเปรียบเทียบสรุป Build Commands

| คำสั่ง | ทำการ Build? | รัน Container? | ใช้ Image ที่มีอยู่แล้ว? | เหมาะกับกรณีใด |
|------|------------|--------------|------------------|--------------|
| docker-compose build | ✅ | ❌ | ❌ | เตรียม image ไว้ล่วงหน้า |
| docker-compose up | ⚠️ (เฉพาะเมื่อไม่มี image) | ✅ | ✅ | รันเร็ว, ไม่มีการแก้ไขโค้ด |
| docker-compose up --build | ✅ (ทุกครั้ง) | ✅ | ❌ | พัฒนาโค้ด, แก้ไขบ่อย |

## 🚨 สิ่งที่ควรคำนึงถึง

1. ในช่วงพัฒนา แนะนำให้ใช้ `docker-compose up --build` เพื่อมั่นใจว่าใช้โค้ดล่าสุดเสมอ

2. เมื่อ deploy ในสภาพแวดล้อมจริง หากมั่นใจว่า image ไม่มีการเปลี่ยนแปลง สามารถใช้ `docker-compose up -d` เพื่อความเร็วในการรัน

3. ควรใช้ `docker-compose down` เมื่อต้องการทำความสะอาดระบบ แต่ถ้าต้องการกลับมารันใหม่เร็วๆ ให้ใช้ `docker-compose stop`