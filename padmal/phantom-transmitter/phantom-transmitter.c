#include "contiki.h"
#include "net/netstack.h"
#include "net/nullnet/nullnet.h"
#include "packetbuf.h"
#include <string.h>
#include <stdio.h>

#include "dev/serial-line.h"
#include "dev/leds.h"

#include "sys/log.h"

#define LOG_MODULE "Phantom Tx"
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
  int channel;

  static char message[3];
  static unsigned count = 0;

  PROCESS_BEGIN();

  /* Initialize NullNet */
  nullnet_buf = (uint8_t *) &message;
  nullnet_len = sizeof(message);

  etimer_set(&periodic_timer, SEND_INTERVAL);

  // Reference: arch/dev/radio/cc2420/cc2420.c (L.83) & (L.284)
  static int POWER[] = {-25, -15, -10, -7, -5, -3, -1, 0};
  static int power_pos = 7;

  /*
  |     2     |  1  |   2   |   8   |   2   |   8   |  21   |   VAR   |  2  |
  | FrameCTRL | Seq | D PAN | D ADD | S PAN | S ADD | AUX H | PAYLOAD | FCS |
  */

  while (1) {
    PROCESS_WAIT_EVENT();

    if (ev == serial_line_event_message) {
      char CH = *(char *) data;
      switch (CH) {
        case '\0': // Log status
          NETSTACK_CONF_RADIO.get_value(RADIO_PARAM_TXPOWER, &power);
          NETSTACK_CONF_RADIO.get_value(RADIO_PARAM_CHANNEL, &channel);
          LOG_INFO("TX Power is %d dBm\n", power);
          LOG_INFO("Channel is %d\n", channel);
          break;
        case 'r': // Packet counter reset
          LOG_INFO("Packet count reset\n");
          NETSTACK_CONF_RADIO.set_value(RADIO_PARAM_TXPOWER, POWER[power_pos]);
          NETSTACK_CONF_RADIO.get_value(RADIO_PARAM_TXPOWER, &power);
          LOG_INFO("TX Power is at %d dBm\n", power);
          count = 0;
          leds_off(LEDS_ALL); leds_off(LEDS_RED);
          break;
        case 'R': // Full reset
          LOG_INFO("Full reset; max power\n");
          power_pos = 7;
          NETSTACK_CONF_RADIO.set_value(RADIO_PARAM_TXPOWER, POWER[7]);
          NETSTACK_CONF_RADIO.get_value(RADIO_PARAM_TXPOWER, &power);
          LOG_INFO("TX Power is reset to %d dBm\n", power);
          count = 0;
          leds_off(LEDS_ALL); leds_off(LEDS_RED);
          break;
        case 'w': // Increase power
          power_pos++;
          if (power_pos == 8) {
            power_pos = 7;
          }
          NETSTACK_CONF_RADIO.set_value(RADIO_PARAM_TXPOWER, POWER[power_pos]);
          NETSTACK_CONF_RADIO.get_value(RADIO_PARAM_TXPOWER, &power);
          LOG_INFO("TX Power is increased to %d dBm\n", power);
          break;
        case 's': // Decrease power
          power_pos--;
          if (power_pos == -1) {
            power_pos = 0;
          }
          NETSTACK_CONF_RADIO.set_value(RADIO_PARAM_TXPOWER, POWER[power_pos]);
          NETSTACK_CONF_RADIO.get_value(RADIO_PARAM_TXPOWER, &power);
          LOG_INFO("TX Power is decreased to %d dBm\n", power);
          break;
        default:
          LOG_INFO("Invalid command.\n");
          LOG_INFO("w: increase power\n");
          LOG_INFO("s: decrease power\n");
          LOG_INFO("\\n: query channel and power\n");
          LOG_INFO("r: reset packet counter\n");
          LOG_INFO("R: full reset\n");
          break;
      }
    }
    else if (ev == PROCESS_EVENT_TIMER) {
      if (count < MESSAGE_COUNT) {
        memcpy(nullnet_buf, &count, sizeof(count));
        nullnet_len = sizeof(count);

        NETSTACK_NETWORK.output(NULL);
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