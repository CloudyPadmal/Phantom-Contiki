#include "contiki.h"
#include "net/netstack.h"
#include "net/nullnet/nullnet.h"
#include "packetbuf.h"
#include <string.h>
#include <stdio.h>

#include "dev/serial-line.h"
#include "dev/leds.h"

#include "sys/log.h"
#define LOG_MODULE "Eavesdrop"
#define LOG_LEVEL LOG_LEVEL_INFO

/* Configuration */
#define SEND_INTERVAL (CLOCK_SECOND)

PROCESS(eaves_node, "Fast Eavesdropper");
AUTOSTART_PROCESSES(&eaves_node);

/*--------------------------------------------------------------------------------------------------------------------*/
void message_received(const void *data, uint16_t len, const linkaddr_t *src, const linkaddr_t *dest) {
  int16_t packet_rssi = packetbuf_attr(PACKETBUF_ATTR_RSSI);
  int16_t packet_lqi = packetbuf_attr(PACKETBUF_ATTR_LINK_QUALITY);

  unsigned count;
  memcpy(&count, data, sizeof(count));
  LOG_INFO("Received %u from ", count);
  LOG_INFO_LLADDR(src);
  LOG_INFO_(" [RSSI: %d", packet_rssi);
  LOG_INFO_(" | LQI: %d]", packet_lqi);
  LOG_INFO_("\n");
  leds_toggle(LEDS_RED);
  leds_toggle(LEDS_YELLOW);
}

/*--------------------------------------------------------------------------------------------------------------------*/
PROCESS_THREAD(eaves_node, ev, data) {
  static struct etimer periodic_timer;

  PROCESS_BEGIN();

  /* Initialize NullNet */
  nullnet_set_input_callback(message_received);

  etimer_set(&periodic_timer, SEND_INTERVAL);

  /*
  |     2     |  1  |   2   |   8   |   2   |   8   |  21   |   VAR   |  2  |
   Frame CTRL | Seq | D PAN | D ADD | S PAN | S ADD | AUX H | PAYLOAD | FCS |
  */

  leds_on(LEDS_RED);
  leds_off(LEDS_YELLOW);

  while (1) {
    PROCESS_WAIT_EVENT();
    if (ev == PROCESS_EVENT_TIMER) etimer_reset(&periodic_timer);
  }

  PROCESS_END();
}