#include <fcntl.h>
#include <sys/sendfile.h>
void main() {
  sendfile(1, open("/flag", 0), 0, 0x100);
}
