pylibsalt
=========

SaLT python library.

Used by `Salix Live Installer`_ and Bootsetup_.

:Copyright: 2011-2014, Salix OS
:License: `GPL version 2`__ (or at your option, any later version)

__ LICENSE

Features
--------

- chroot function
- execute functions (checkRoot execCall execCheck execGetOutput)
- disk functions (getDiskInfo getDisks getPartitionInfo getPartitions getSwapPartitions)
- filesystem functions (getFsLabel getFsType makeFs)
- freesize functions (getBlockSize getHumanSize getSizes getUsedSize)
- fstab functions (addFsTabEntry createFsTab)
- kernel parameters functions (getKernelParamValue hasKernelParam)
- mounting functions (getMountPoint getTempMountDir isMounted mountDevice umountDevice)
- system users functions (changePasswordSystemUser checkPasswordSystemUser createSystemUser deleteSystemUser listRegularSystemUsers)
- timezone functions (getDefaultTimeZone isNTPEnabledByDefault listTZCities listTZContinents listTimeZones setDefaultTimeZone setNTPDefault)
- languages functions (getCurrentLocale getDefaultLocale listAvailableLocales setDefaultLocale)
- keyboards functions (findCurrentKeymap isIbusEnabledByDefault isNumLockEnabledByDefault listAvailableKeymaps setDefaultKeymap setIbusDefault setNumLockDefault)

.. _`Salix Live Installer`: https://github.com/Salix-OS/salix-live-installer
.. _Bootsetup: https://github.com/jrd/bootsetup
