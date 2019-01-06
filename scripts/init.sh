git submodule init
git submodule update

cd material-component-android
git config core.sparsecheckout true
echo lib/java/com/google/android/material/ > ../.git/modules/material-component-android/info/sparse-checkout
git read-tree -mu HEAD
cd ../

cd platform_frameworks_support
git config core.sparsecheckout true
echo appcompat/res/ > ../.git/modules/platform_frameworks_support/info/sparse-checkout
git read-tree -mu HEAD
cd ../
