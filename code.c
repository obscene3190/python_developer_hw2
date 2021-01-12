#include <MSP430.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>

#define MAX			10
#define R			BIT0
#define	G			BIT1
#define	B			BIT2
#define TXD 		BIT4
#define RXD 		BIT5
#define Rt			TA0CCR1
#define Gt			TA0CCR2
#define Bt			TA1CCR1


uint8_t uartBuf;
uint32_t	tmp;

// инициализация UART для скорости 9600
void UART_init() {
	P3SEL |= RXD | TXD;
	UCA0CTL1 |= UCSWRST;
	UCA0CTL1 |= UCSSEL_2; // SMCLK
	UCA0BR0 = 104; // 1MHz/9600 = 104
	UCA0BR1 = 0x00; // 1MHz 9600
	UCA0MCTL = UCBRS2 + UCBRS0; // Modulation UCBRSx = 5
	UCA0CTL1 &= ~UCSWRST; // **Initialize USCI state machine**
}

// Включение на запись
void UART_write_enable() {
	UC0IE &= ~UCA0RXIE;
	IE2 &= ~UCA0RXIE;
	IE2 |= UCA0TXIE;
}

// Включение на чтение
void UART_read_enable() {
	IE2 &= ~UCA0TXIE;
	IE2 |= UCA0RXIE;
}

// чтение байта по UART
uint8_t UART_read_byte() {
	UART_read_enable();
	return uartBuf;
}

// нормировка rgb
uint32_t norm(uint32_t num) {
	tmp = ( (num*999)/255);
	return tmp;
}

// Назначение делитилей таймера для задания ШИМ
void set_color(uint32_t r, uint32_t g, uint32_t b) {
	TA0CCR1 = norm(r);
	TA0CCR2 = norm(g);
	TA1CCR1 = norm(b);
}


int main (void) {

	WDTCTL = WDTPW | WDTHOLD;

	DCOCTL = CALDCO_1MHZ;
	BCSCTL1 = CALBC1_1MHZ;
	
	// конфигурируем таймеры для задания ШИМ ргб
	// используем выходы таймера для каждого из R, G, B

	P1DIR |= 0x0C;                   // P1.2 and P1.3 output
	P1SEL |= 0x0C; 

	TA0CCR0 = 1000;    
	TA0CCR1 = 0;               
	TA0CCTL1 = OUTMOD_7;            
	TA0CCR2 = 0;               
	TA0CCTL2 = OUTMOD_7;              
	TA0CTL = TASSEL_2 + MC_1;       // ACLK, cont mode

	P3DIR |= 0x80;                  
	P3SEL |= 0x80;

	TA1CCR0 = 1000;          
	TA1CCR1 = 0;               
	TA1CCTL1 = OUTMOD_7;              
	TA1CTL = TASSEL_2 + MC_1;       // ACLK, cont mode

	// конфигурируем UART
	IFG2 = 0x00;
	UC0IE |= UCA0RXIE; // Enable USCI_A0 RX interrupt
	IE2 |= UCA0RXIE;
	UART_init();

	// порт 1 на выход
	P1DIR = 0xFF;
	uint8_t message;

	__bis_SR_register(GIE);
	while (1) {
		// ожидаем команду пользователя
		__bis_SR_register(LPM0_bits);
		// принимаем сообщение
		message = (char) UART_read_byte();
		// меняем цвет в зависимости от сообщения

		/*
		TA0CCR1 - R
		TA0CCR2 - G
		TA1CCR1 - B
		*/

		// смотрим на полученное сообщение
		switch (message)
		{
			case 'r':
				set_color(255,0,0);
				break;
			case 'g':
				set_color(0,255,0);
				break;
			case 'b':
				set_color(0,0,255);
				break;
			case '1': //
				set_color(100,60,70);
				break;
			case '2':	// серый
				set_color(220,10,58);
				break;
			case '3': // другой серый
				set_color(90,240,130);
				break;
		}
		// обратно заходим в ЛП0 мод
		
	}
	return 0;
}

// Прерывание UART, где в переменную записывается полученная команда
#pragma vector = USCIAB0RX_VECTOR
__interrupt void RX_ISR_SPI(void) {
    while (UCA0RXIFG & IFG2) {
      uartBuf = UCA0RXBUF;
      __bic_SR_register_on_exit(LPM0_bits);
    }
}
