#include "contiki.h"
#include "net/netstack.h"
#include "net/nullnet/nullnet.h"
#include "packetbuf.h"
#include <string.h>
#include <stdio.h>

#include "dev/serial-line.h"
#include "dev/leds.h"

#include "sys/log.h"

#define LOG_MODULE "Phantm Tx"
#define LOG_LEVEL LOG_LEVEL_INFO

/* Configuration */
#define SEND_INTERVAL (CLOCK_SECOND * 0.1)
#define MESSAGE_COUNT 500

PROCESS(phantom_node, "Phantom Tx");
AUTOSTART_PROCESSES(&phantom_node);

/*---------------------------------------------------------------------------*/
PROCESS_THREAD(phantom_node, ev, data) {
  static struct etimer periodic_timer;

  int power;

  static char message[3];
  static unsigned count = 0;

  PROCESS_BEGIN();

  /* Initialize NullNet */
  nullnet_buf = (uint8_t * ) & message;
  nullnet_len = sizeof(message);

  etimer_set(&periodic_timer, SEND_INTERVAL);

  NETSTACK_CONF_RADIO.set_value(RADIO_PARAM_TXPOWER, 5);
  NETSTACK_CONF_RADIO.get_value(RADIO_PARAM_TXPOWER, &power);

  /*
  |     2     |  1  |   2   |   8   |   2   |   8   |  21   |   VAR   |  2  |
  | FrameCTRL | Seq | D PAN | D ADD | S PAN | S ADD | AUX H | PAYLOAD | FCS |
  */

  while (1) {
    PROCESS_WAIT_EVENT();

    if (ev == serial_line_event_message) {
      char CH = *(char *) data;
      if (CH == '\0') {
        LOG_INFO("Packet count reset\n");
        LOG_INFO("TX Power is set to %d dBm\n", power);
        count = 0;
        leds_off(LEDS_ALL);
      }
    }
    else if (ev == PROCESS_EVENT_TIMER) {
      if (count < MESSAGE_COUNT) {
        memcpy(nullnet_buf,&count, sizeof(count));
        nullnet_len = sizeof(count);

        NETSTACK_NETWORK.
        output(NULL);
        count++;

        leds_toggle(LEDS_YELLOW);

        if (count % 10 == 0) {
          leds_toggle(LEDS_GREEN);
        }
      }
      else {
        // Indicates that transmission is complete
        leds_on(LEDS_RED);
        leds_on(LEDS_GREEN);
        leds_on(LEDS_YELLOW);
      }
    etimer_reset(&periodic_timer);
    }
  }

  PROCESS_END();

}