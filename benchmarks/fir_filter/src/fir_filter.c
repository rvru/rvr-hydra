/*
 * fir_filter.c
 *
 *  Created on: Oct 23, 2019
 *      Author: jhellar
 *
 *  Correct output:
 *      [2, 13, 27, 43, 76, 68, 110, 84, 102, 81,
 *       77, 72, 80, 79, 85, 87, 82, 83, 96, 72,
 *       120, 75, 102, 71, 60, 43, 29, 12, 9, 3]
 */

#define ITERATIONS  10

#define DATA_LEN    21
#define FILT_LEN    10
#define OUT_LEN     (DATA_LEN + FILT_LEN - 1) // = 30

int main(void)
{
    // Initialize arrays (32-bit data and coeff)
    static int coeff[OUT_LEN] = {1, 4, 2, 7, 3,
                            5, 3, 2, 1, 1};
    static int data[OUT_LEN] = {2, 5, 3,
                           7, 1, 4,
                           3, 2, 1,
                           1, 3, 6,
                           5, 1, 1,
                           3, 2, 8,
                           0, 6, 3};
    volatile int output[OUT_LEN];

    // Initialize pointers
    int *data_ptr;
    int *coeff_ptr;
    volatile int *output_ptr = output;

    int acc;
    int i, j, k;

    /* FIR Filter: coeff array fixed, data ptr circularly shifts */
    for (j = 0; j < ITERATIONS; j++) {
        for (i = 0; i < OUT_LEN; i++) {         // for each y[i]
            acc = 0;
            coeff_ptr = &coeff[0];                  // coeff[0]
            data_ptr = &data[0] + i;                // data[i]
            for (k = 0; k < OUT_LEN; k++){      // for each coeff[k]
                // coeff[k] * data[i - k]
                acc += (*coeff_ptr++) * (*data_ptr--);
                if (data_ptr < &data[0]) {          // circular shift
                    data_ptr = &data[OUT_LEN - 1];
                }
            }
            *(output_ptr + i) = acc;
        }
    }

    return 0;

}
