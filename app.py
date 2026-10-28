from flask import Flask, render_template, request, redirect, url_for
import math

app = Flask(__name__)


def doi_sang_so(chuoi):
    """Đổi '2,5' hoặc '2.5' thành số; trả về None nếu không hợp lệ."""
    try:
        so = float(chuoi.strip().replace(",", "."))
        if math.isfinite(so):
            return so
    except (ValueError, OverflowError):
        pass
    return None


def kiem_tra_diem(chuoi, ten_o):
    """Hàm kiểm tra dùng chung cho 3 ô điểm ở bài 2."""
    if chuoi.strip() == "":
        return None, f"Lỗi ô {ten_o}: Vui lòng nhập điểm."

    diem = doi_sang_so(chuoi)
    if diem is None:
        return None, f"Lỗi ô {ten_o}: Vui lòng nhập một số."
    if diem < 0 or diem > 10:
        return None, f"Lỗi ô {ten_o}: Điểm phải từ 0 đến 10."
    return diem, ""


@app.route("/")
def trang_chu():
    return redirect(url_for("bai1"))


@app.route("/bai1", methods=["GET", "POST"])
def bai1():
    a = ""
    b = ""
    op = "+"
    loi_a = ""
    loi_b = ""
    loi_op = ""
    ket_qua = ""

    if request.method == "POST":
        a = request.form.get("a", "")
        b = request.form.get("b", "")
        op = request.form.get("op", "")

        so_a = doi_sang_so(a)
        so_b = doi_sang_so(b)

        if so_a is None:
            loi_a = "Lỗi ô a: Vui lòng nhập một số."
        if so_b is None:
            loi_b = "Lỗi ô b: Vui lòng nhập một số."
        if op not in ["+", "-", "*", "/"]:
            loi_op = "Phép toán không hợp lệ."

        if not loi_a and not loi_b and not loi_op:
            if op == "+":
                kq = so_a + so_b
            elif op == "-":
                kq = so_a - so_b
            elif op == "*":
                kq = so_a * so_b
            else:
                if so_b == 0:
                    loi_b = "Lỗi ô b: Không thể chia cho 0."
                else:
                    kq = so_a / so_b

            if not loi_b:
                ket_qua = f"{so_a:g} {op} {so_b:g} = {kq:g}"

    return render_template("bai1.html", a=a, b=b, op=op,
                           loi_a=loi_a, loi_b=loi_b,
                           loi_op=loi_op, ket_qua=ket_qua)


@app.route("/bai2", methods=["GET", "POST"])
def bai2():
    cc = ""
    gk = ""
    ck = ""
    loi_cc = ""
    loi_gk = ""
    loi_ck = ""
    ket_qua = ""

    if request.method == "POST":
        cc = request.form.get("cc", "")
        gk = request.form.get("gk", "")
        ck = request.form.get("ck", "")

        diem_cc, loi_cc = kiem_tra_diem(cc, "CC")
        diem_gk, loi_gk = kiem_tra_diem(gk, "GK")
        diem_ck, loi_ck = kiem_tra_diem(ck, "CK")

        if not loi_cc and not loi_gk and not loi_ck:
            diem = round(diem_cc * 0.1 + diem_gk * 0.3 + diem_ck * 0.6, 1)

            if diem_ck < 1:
                diem_chu = "F (điểm thi dưới 1)"
            elif diem >= 8.5:
                diem_chu = "A"
            elif diem >= 7.0:
                diem_chu = "B"
            elif diem >= 5.5:
                diem_chu = "C"
            elif diem >= 4.0:
                diem_chu = "D"
            else:
                diem_chu = "F"

            ket_qua = f"{diem:.1f} - {diem_chu}"

    return render_template("bai2.html", cc=cc, gk=gk, ck=ck,
                           loi_cc=loi_cc, loi_gk=loi_gk,
                           loi_ck=loi_ck, ket_qua=ket_qua)


@app.route("/bai3", methods=["GET", "POST"])
def bai3():
    cao = ""
    nang = ""
    loi_cao = ""
    loi_nang = ""
    ket_qua = ""
    mau = ""
    goi_y = ""

    if request.method == "POST":
        cao = request.form.get("cao", "")
        nang = request.form.get("nang", "")

        so_cao = doi_sang_so(cao)
        so_nang = doi_sang_so(nang)

        if so_cao is None:
            loi_cao = "Lỗi ô chiều cao: Vui lòng nhập một số."
        elif so_cao < 50 or so_cao > 250:
            loi_cao = "Lỗi ô chiều cao: Giá trị phải từ 50 đến 250 (nhập cm, không phải mét)."

        if so_nang is None:
            loi_nang = "Lỗi ô cân nặng: Vui lòng nhập một số."
        elif so_nang < 10 or so_nang > 300:
            loi_nang = "Lỗi ô cân nặng: Giá trị phải từ 10 đến 300."

        if not loi_cao and not loi_nang:
            cao_m = so_cao / 100
            bmi = round(so_nang / (cao_m * cao_m), 1)

            if bmi < 18.5:
                loai = "Thiếu cân"
                mau = "vang"
            elif bmi < 23:
                loai = "Bình thường"
                mau = "xanh"
            elif bmi < 25:
                loai = "Thừa cân"
                mau = "vang"
            else:
                loai = "Béo phì"
                mau = "do"

            can_nang_min = 18.5 * cao_m * cao_m
            can_nang_max = 22.9 * cao_m * cao_m
            ket_qua = f"BMI = {bmi:.1f} - {loai}"
            goi_y = f"Cân nặng nên có: {can_nang_min:.1f} - {can_nang_max:.1f} kg"

    return render_template("bai3.html", cao=cao, nang=nang,
                           loi_cao=loi_cao, loi_nang=loi_nang,
                           ket_qua=ket_qua, mau=mau, goi_y=goi_y)


if __name__ == "__main__":
    app.run(debug=True)
