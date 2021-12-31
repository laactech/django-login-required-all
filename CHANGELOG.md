## 1.1.2

* Added Django 4.0 support

## 1.1.1

* Fixing issue where `re.compile('^/.+$')` is added to `LoginRequiredMiddleware.public_view_urls` when `DEBUG` is set to
  true and `MEDIA_URL` is not defined (Thanks to Bernard)

## 1.1.0

* Changing max version restriction for Django from 3.0 to 4.0
* Dropping official support for Python 3.5 to follow Django's release cycle
    * Note: the packages source has not been significantly changed and should still work
* Dropping official support for Django 1.11, 2.0, and 2.1 to follow Django's release cycle
    * Note: the packages source has not been significantly changed and should still work
* Adding testing for Django 3.1
* Dropping testing for unsupported versions

## 1.0.2

* Add Python 3.8 and Django 3.0 support

## 1.0.1

* Update PYPI readme

## 1.0.0

* Stable release of fork