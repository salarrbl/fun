import os
import subprocess
import time

# تابع برای اجرای دستورات در شل
def run_command(command):
    try:
        print(f"Running command: {command}")
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        exit(1)

# تابع برای آماده‌سازی پارتیشن‌ها
def partition_disks():
    print("Partitioning disks...")
    # جایگزین کردن دستورات برای پارتیشن‌بندی
    run_command("parted /dev/sda -- mklabel gpt")
    run_command("parted /dev/sda -- mkpart primary ext4 0% 100%")
    run_command("mkfs.ext4 /dev/sda1")
    run_command("mount /dev/sda1 /mnt/gentoo")

# تابع برای نصب سیستم پایه
def install_base_system():
    print("Installing base system...")
    run_command("wget http://distfiles.gentoo.org/releases/amd64/autobuilds/latest-stage3-amd64.tar.xz -O /mnt/gentoo/stage3.tar.xz")
    run_command("tar xpvf /mnt/gentoo/stage3.tar.xz -C /mnt/gentoo --xattrs-include='*.*' --numeric-owner")
    run_command("mount --types proc /proc /mnt/gentoo/proc")
    run_command("mount --rbind /sys /mnt/gentoo/sys")
    run_command("mount --make-rslave /mnt/gentoo/sys")
    run_command("mount --rbind /dev /mnt/gentoo/dev")
    run_command("mount --make-rslave /mnt/gentoo/dev")
    run_command("cp --dereference /etc/resolv.conf /mnt/gentoo/etc/")

# تابع برای انتخاب پروفایل
def select_profile():
    print("Selecting system profile...")
    run_command("chroot /mnt/gentoo eselect profile list")
    run_command("chroot /mnt/gentoo eselect profile set 1")

# تابع برای نصب کرنل و پیکربندی آن
def install_kernel():
    print("Installing kernel...")
    run_command("chroot /mnt/gentoo emerge sys-kernel/gentoo-sources")
    run_command("chroot /mnt/gentoo genkernel all")

# تابع برای نصب GRUB و پیکربندی آن
def install_grub():
    print("Installing GRUB...")
    run_command("chroot /mnt/gentoo emerge sys-boot/grub:2")
    run_command("chroot /mnt/gentoo grub-install /dev/sda")
    run_command("chroot /mnt/gentoo grub-mkconfig -o /boot/grub/grub.cfg")

# تابع برای ایجاد یوزر
def create_user():
    print("Creating user...")
    run_command("chroot /mnt/gentoo useradd -m -G users,wheel,audio,video -s /bin/bash your_username")
    run_command("chroot /mnt/gentoo echo 'your_username:your_password' | chpasswd")
    run_command("chroot /mnt/gentoo echo '%wheel ALL=(ALL) ALL' >> /etc/sudoers")

# تابع برای پیکربندی شبکه
def configure_network():
    print("Configuring network...")
    run_command("chroot /mnt/gentoo emerge net-misc/dhcpcd")
    run_command("chroot /mnt/gentoo rc-update add dhcpcd default")

# تابع برای تنظیم رمز عبور root
def set_root_password():
    print("Setting root password...")
    run_command("chroot /mnt/gentoo echo 'root:your_root_password' | chpasswd")

# تابع برای خروج از chroot و انجام مراحل نهایی
def final_steps():
    print("Exiting chroot and performing final steps...")
    run_command("exit")
    print("Installation complete! Please reboot your system.")

# تابع اصلی که تمام مراحل نصب را به ترتیب انجام می‌دهد
def install_gentoo():
    partition_disks()
    install_base_system()
    select_profile()
    install_kernel()
    install_grub()
    create_user()
    configure_network()
    set_root_password()
    final_steps()

if __name__ == "__main__":
    install_gentoo()

