include $(TOPDIR)/rules.mk

PKG_NAME:=uugamebooster
PKG_VERSION:=4.12.12
PKG_RELEASE:=1

PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION)-$(ARCH).tar.gz
PKG_SOURCE_URL:=https://uu.gdl.netease.com/uuplugin/openwrt-$(ARCH)/v$(PKG_VERSION)/uu.tar.gz?
ifeq ($(ARCH),aarch64)
  PKG_HASH:=273884e9d05d6d8869a2b9d36425a01588949f27da200754cefff42ea2440c23
else ifeq ($(ARCH),arm)
  PKG_HASH:=9004210bc99c81351949e897a409c41b6295277f08f956f8520bec34b3f4cb58
else ifeq ($(ARCH),mipsel)
  PKG_HASH:=5dffbc1677c1d201be4b960e1f00927a6c6c34691da4a4d5612346d5f27ee08d
else ifeq ($(ARCH),x86_64)
  PKG_HASH:=a8283f5316bc48b19b7d3bedc833407925d483ab16a1a02fe55dec6c3ac9700c
endif

include $(INCLUDE_DIR)/package.mk

STRIP:=true

TAR_CMD=$(HOST_TAR) -C $(1)/ $(TAR_OPTIONS)

define Package/uugamebooster
  SECTION:=net
  CATEGORY:=Network
  DEPENDS:=@(aarch64||arm||mipsel||x86_64) +kmod-tun
  TITLE:=NetEase UU Game Booster
  URL:=https://uu.163.com
endef

define Package/uugamebooster/description
  NetEase's UU Game Booster Accelerates Triple-A Gameplay and Market.
endef

define Build/Compile
endef

define Package/uugamebooster/conffiles
/.uuplugin_uuid
/usr/share/uugamebooster/uu.conf
endef

define Package/uugamebooster/install
	$(INSTALL_DIR) $(1)/usr/bin
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/uuplugin $(1)/usr/bin/uugamebooster

	$(INSTALL_DIR) $(1)/usr/share/uugamebooster
	$(INSTALL_CONF) $(PKG_BUILD_DIR)/uu.conf $(1)/usr/share/uugamebooster/uu.conf

	$(INSTALL_DIR) $(1)/etc/config $(1)/etc/init.d
	$(INSTALL_CONF) ./files/uugamebooster.config $(1)/etc/config/uugamebooster
	$(INSTALL_BIN) ./files/uugamebooster.init $(1)/etc/init.d/uugamebooster
endef

$(eval $(call BuildPackage,uugamebooster))
