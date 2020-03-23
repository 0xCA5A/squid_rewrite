#!/bin/bash
set -e

create_log_dir() {
  mkdir -p "${SQUID_LOG_DIR}"
  chmod -R 755 "${SQUID_LOG_DIR}"
  chown -R "${SQUID_USER}":"${SQUID_USER}" "${SQUID_LOG_DIR}"
}

create_cache_dir() {
  mkdir -p "${SQUID_CACHE_DIR}"
  chown -R "${SQUID_USER}":"${SQUID_USER}" "${SQUID_CACHE_DIR}"
}

create_rewrite_dir() {
  mkdir -p "${SQUID_REWRITE_DIR}"
  chown -R "${SQUID_USER}":"${SQUID_USER}" "${SQUID_REWRITE_DIR}"
}

create_log_dir
create_cache_dir
create_rewrite_dir

if [[ ! -d "${SQUID_CACHE_DIR}/00" ]]; then
  echo "Initializing cache..."
  # Create missing swap directories and other missing cache_dir structures, then exit.
  $(which squid) -N -f "${SQUID_CFG_FILE}" -z
fi

# FIXME: ugly
echo "Starting webserver..."
python3 -m http.server --directory ${SQUID_REWRITE_DIR} 8000 &>/dev/null &

echo "Starting squid..."
exec $(which squid) -f "${SQUID_CFG_FILE}" -NYCd 1 "${SQUID_EXTRA_ARGS}"
