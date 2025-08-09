FROM almalinux:9

# System deps for Python + mysqlclient
RUN dnf -y update && \
    dnf -y install \
      python3 python3-pip python3-devel \
      gcc make \
      mariadb-connector-c mariadb-connector-c-devel \
      pkgconf-pkg-config \
      git && \
    dnf clean all

WORKDIR /app

# (Optional) prevent .pyc and ensure unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

# Upgrade pip then install deps
RUN python3 -m pip install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Copy the rest
COPY . .

# Expose if you run gunicorn inside
EXPOSE 5005

# Example CMD (adjust for your project)
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
