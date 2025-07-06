#!/bin/bash

echo "Starting Django application..."

echo "Waiting for database..."
while ! python src/manage.py check --database default 2>/dev/null; do
  echo "Database is unavailable - sleeping"
  sleep 2
done

echo "Database is ready!"

# Sprawdź czy są niezastosowane migracje
echo "Checking for unapplied migrations..."
UNAPPLIED=$(python src/manage.py showmigrations --plan | grep -c "\\[ \\]")

if [ "$UNAPPLIED" -gt 0 ]; then
    echo "Found $UNAPPLIED unapplied migrations. Running migrate..."
    python src/manage.py migrate --noinput
    #--noinput - nie pytaj o potwierdzenie (automatyczne "tak")

    #$? to specjalna zmienna w Bash, która zawiera kod wyjścia ostatniej komendy(0 - sukces, pozostałe liczby to błędy)
    if [ $? -eq 0 ]; then
        echo "Migrations applied successfully!"
    else
        echo "Migration failed! Exiting..."
        exit 1
    fi
else
    echo "No migrations needed."
fi

echo "Starting Django development server..."
exec python src/manage.py runserver 0.0.0.0:8100