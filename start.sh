#!/bin/bash

# Script de démarrage pour l'application ecommerce
# Usage: ./start.sh [dev|prod]

set -e

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  ECOMMERCE MICROSERVICES${NC}"
    echo -e "${BLUE}================================${NC}"
}

# Fonction pour vérifier Docker
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker n'est pas installé. Veuillez installer Docker."
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose n'est pas installé. Veuillez installer Docker Compose."
        exit 1
    fi

    if ! docker info &> /dev/null; then
        print_error "Docker n'est pas démarré. Veuillez démarrer Docker."
        exit 1
    fi
}

# Fonction pour arrêter les conteneurs existants
stop_existing_containers() {
    print_message "Arrêt des conteneurs existants..."
    docker-compose down 2>/dev/null || true
    docker-compose -f docker-compose.dev.yml down 2>/dev/null || true
}

# Fonction pour démarrer en mode production
start_production() {
    print_message "Démarrage en mode PRODUCTION..."
    
    # Vérifier les ports
    check_ports
    
    # Construire et démarrer les services
    docker-compose up --build -d
    
    print_message "Services démarrés en arrière-plan"
    print_message "Application disponible sur: http://localhost"
    print_message "Backend API: http://localhost:8000"
    print_message "Frontend: http://localhost:3000"
    print_message "Prometheus: http://localhost:9090"
    
    # Attendre que les services soient prêts
    wait_for_services
}

# Fonction pour démarrer en mode développement
start_development() {
    print_message "Démarrage en mode DÉVELOPPEMENT..."
    
    # Vérifier les ports
    check_ports
    
    # Construire et démarrer les services
    docker-compose -f docker-compose.dev.yml up --build -d
    
    print_message "Services de développement démarrés"
    print_message "Frontend: http://localhost:3000 (avec hot-reload)"
    print_message "Backend: http://localhost:8000 (avec hot-reload)"
    print_message "Base de données: localhost:5432"
    
    # Attendre que les services soient prêts
    wait_for_services_dev
}

# Fonction pour vérifier les ports
check_ports() {
    local ports=(80 3000 8000 5432 6379 9090 9200)
    
    for port in "${ports[@]}"; do
        if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
            print_warning "Le port $port est déjà utilisé"
        fi
    done
}

# Fonction pour attendre que les services soient prêts (production)
wait_for_services() {
    print_message "Attente que les services soient prêts..."
    
    # Attendre la base de données
    print_message "Attente de la base de données..."
    timeout 60 bash -c 'until docker-compose exec -T db pg_isready -U ecommerce_user -d ecommerce_db; do sleep 2; done' || {
        print_error "La base de données n'est pas prête"
        exit 1
    }
    
    # Attendre le backend
    print_message "Attente du backend..."
    timeout 60 bash -c 'until curl -f http://localhost:8000/health/ 2>/dev/null; do sleep 2; done' || {
        print_warning "Le backend n'est pas encore prêt"
    }
    
    # Attendre le frontend
    print_message "Attente du frontend..."
    timeout 60 bash -c 'until curl -f http://localhost 2>/dev/null; do sleep 2; done' || {
        print_warning "Le frontend n'est pas encore prêt"
    }
    
    print_message "Tous les services sont prêts!"
}

# Fonction pour attendre que les services soient prêts (développement)
wait_for_services_dev() {
    print_message "Attente que les services de développement soient prêts..."
    
    # Attendre la base de données
    print_message "Attente de la base de données..."
    timeout 60 bash -c 'until docker-compose -f docker-compose.dev.yml exec -T db pg_isready -U ecommerce_user -d ecommerce_db; do sleep 2; done' || {
        print_error "La base de données n'est pas prête"
        exit 1
    }
    
    # Attendre le backend
    print_message "Attente du backend..."
    timeout 60 bash -c 'until curl -f http://localhost:8000/health/ 2>/dev/null; do sleep 2; done' || {
        print_warning "Le backend n'est pas encore prêt"
    }
    
    # Attendre le frontend
    print_message "Attente du frontend..."
    timeout 60 bash -c 'until curl -f http://localhost:3000 2>/dev/null; do sleep 2; done' || {
        print_warning "Le frontend n'est pas encore prêt"
    }
    
    print_message "Tous les services de développement sont prêts!"
}

# Fonction pour afficher l'aide
show_help() {
    echo "Usage: $0 [dev|prod|stop|logs|status|clean]"
    echo ""
    echo "Commandes:"
    echo "  dev     - Démarrer en mode développement"
    echo "  prod    - Démarrer en mode production"
    echo "  stop    - Arrêter tous les services"
    echo "  logs    - Afficher les logs"
    echo "  status  - Afficher le statut des services"
    echo "  clean   - Nettoyer les conteneurs et volumes"
    echo "  help    - Afficher cette aide"
    echo ""
    echo "Mode par défaut: production"
}

# Fonction pour arrêter les services
stop_services() {
    print_message "Arrêt des services..."
    docker-compose down
    docker-compose -f docker-compose.dev.yml down
    print_message "Services arrêtés"
}

# Fonction pour afficher les logs
show_logs() {
    print_message "Affichage des logs..."
    docker-compose logs -f
}

# Fonction pour afficher le statut
show_status() {
    print_message "Statut des services:"
    docker-compose ps
    echo ""
    print_message "Statut des services de développement:"
    docker-compose -f docker-compose.dev.yml ps
}

# Fonction pour nettoyer
clean_all() {
    print_warning "Nettoyage de tous les conteneurs et volumes..."
    docker-compose down -v
    docker-compose -f docker-compose.dev.yml down -v
    docker system prune -f
    print_message "Nettoyage terminé"
}

# Script principal
main() {
    print_header
    
    # Vérifier Docker
    check_docker
    
    # Traiter les arguments
    case "${1:-prod}" in
        "dev")
            stop_existing_containers
            start_development
            ;;
        "prod")
            stop_existing_containers
            start_production
            ;;
        "stop")
            stop_services
            ;;
        "logs")
            show_logs
            ;;
        "status")
            show_status
            ;;
        "clean")
            clean_all
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            print_error "Option invalide: $1"
            show_help
            exit 1
            ;;
    esac
}

# Exécuter le script principal
main "$@" 