
function updateClock() {
    const now = new Date();
      // نمایش تاریخ و زمان به‌صورت فارسی
    const formatted = now.toLocaleString("fa-IR");
    document.getElementById("datetime").innerText = " " + formatted;
}

    // یک‌بار در شروع:
updateClock();
    // هر ۱۰۰۰ میلی‌ثانیه (۱ ثانیه) تکرا
    // 
setInterval(updateClock, 1000);
