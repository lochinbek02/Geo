set -e

HOST="$1"
shift
PORT="$1"
shift
cmd="$@"

until nc -z "$HOST" "$PORT"; do
  >&2 echo "Waiting for $HOST:$PORT to be available..."
  sleep 1
done

>&2 echo "$HOST:$PORT is available - executing command"
exec $cmd