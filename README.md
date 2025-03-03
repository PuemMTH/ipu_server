# IPU Server

## ข้อกำหนดเบื้องต้น

- ติดตั้ง Docker บนเครื่องของคุณ ([ดาวน์โหลด Docker](https://www.docker.com/get-started))

## การ Build Docker Image

1. เปิด Terminal หรือ Command Prompt
2. นำทางไปยังไดเรกทอรีของโปรเจค
```bash
cd /path/to/ipu_server
```
3. สร้าง Docker image
```bash
docker build -t ipu-server .
```

## การ Run Container

หลังจาก build image เสร็จเรียบร้อย คุณสามารถ run container ได้ด้วยคำสั่ง:

```bash
docker run -p 8080:80 -d --name ipu-container ipu-server
```

คำอธิบาย:
- `-p 8080:80`: Port forwarding จาก port 8080 host_port:container_port บนเครื่อง host ไปยัง port 80 ของ container
- `-d`: Run container ในโหมด detached (background)
- `--name ipu-container`: กำหนดชื่อให้กับ container
- `ipu-server`: ชื่อของ image ที่จะใช้

## การเข้าถึง Application

หลังจาก run container เสร็จเรียบร้อย คุณสามารถเข้าถึง application ได้ที่:

```
http://localhost:8080
```

## คำสั่งที่มีประโยชน์

### ดู container ที่กำลัง run อยู่
```bash
docker ps
```

### หยุดการทำงานของ container
```bash
docker stop ipu-container
```

### เริ่มการทำงานของ container ที่หยุดไป
```bash
docker start ipu-container
```

### ลบ container
```bash
docker rm ipu-container
```

### ดู logs
```bash
docker logs ipu-container
```
