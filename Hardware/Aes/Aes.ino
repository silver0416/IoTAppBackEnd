#include <string.h>
#include "esp_log.h"
#include "mbedtls/cipher.h"

const char *TAG = "esptouch decrypt";

static int decrypt_parameter(const unsigned char *ciphertext, const unsigned char *key, size_t len, unsigned char *plaintext)
{
  int r;
  size_t olen;
  mbedtls_cipher_context_t ctx;
  const mbedtls_cipher_info_t *info = mbedtls_cipher_info_from_type(MBEDTLS_CIPHER_AES_128_ECB);

  if (len % 16 != 0)
  {
    ESP_LOGE(TAG, "len must be a multiple of block size");
    return -1;
  }

  mbedtls_cipher_init(&ctx);

  r = mbedtls_cipher_setup(&ctx, info);
  if (r != 0)
  {
    ESP_LOGE(TAG, "mbedtls_cipher_setup failed -%x", -r);
    goto done;
  }

  r = mbedtls_cipher_setkey(&ctx, key, 128, MBEDTLS_DECRYPT);
  if (r != 0)
  {
    ESP_LOGE(TAG, "mbedtls_cipher_setkey failed -%x", -r);
    goto done;
  }

  r = mbedtls_cipher_reset(&ctx);
  if (r != 0)
  {
    ESP_LOGE(TAG, "mbedtls_cipher_reset failed -%x", -r);
    goto done;
  }

  olen = 0;
  for (int i = 0; i < len; i += 16)
  {
    size_t olen_block = 16;
    r = mbedtls_cipher_update(&ctx, ciphertext + i, 16, plaintext + i, &olen_block);
    if (r != 0)
    {
      ESP_LOGE(TAG, "mbedtls_cipher_update failed -%x", -r);
      goto done;
    }
    olen += olen_block;
  }

  // ESP_LOG_BUFFER_HEX(TAG, plaintext, olen);

  // Check and remove PKCS7 padding
  uint8_t pad_len = plaintext[olen - 1];
  uint8_t dlen = olen - pad_len;
  if (pad_len >= olen || dlen >= olen)
  {
    ESP_LOGE(TAG, "Bad PKCS7 padding byte: %d", pad_len);
    r = MBEDTLS_ERR_CIPHER_INVALID_PADDING;
    goto done;
  }
  for (int i = dlen; i < olen; i++)
  {
    if (plaintext[i] != pad_len)
    {
      ESP_LOGE(TAG, "Bad PKCS7 padding byte at offset %d", i);
      r = MBEDTLS_ERR_CIPHER_INVALID_PADDING;
      goto done;
    }
    plaintext[i] = 0;
  }

  ESP_LOGI(TAG, "decrypt successful");
  r = dlen;

done:
  mbedtls_cipher_free(&ctx);
  return r;
}

void app_main()
{
  const unsigned char key[16] = "secret key!!"; // will 0-pad to 16 bytes
  unsigned char ciphertext[32] = {
      0x1a,
      0x8a,
      0x97,
      0x89,
      0xb7,
      0x1e,
      0xa4,
      0x36,
      0x08,
      0x53,
      0x25,
      0x21,
      0x5d,
      0x53,
      0xe5,
      0x0d,
      0x77,
      0x67,
      0x8b,
      0xa1,
      0xde,
      0x56,
      0x38,
      0xdb,
      0x20,
      0x0e,
      0x52,
      0xf4,
      0x60,
      0xe8,
      0xfa,
      0xd2,
  };
  unsigned char plaintext[32] = {0}; // note: must be same size as ciphertext buffer

  int r = decrypt_parameter(ciphertext, key, sizeof(ciphertext), plaintext);
  ESP_LOGI(TAG, "decrypt result %d", r);
  ESP_LOGI(TAG, "plaintext as a string: %s\n", plaintext);
  printf("Done");
}