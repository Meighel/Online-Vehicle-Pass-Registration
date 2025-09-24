class NotificationManager {
    constructor() {
        this.pollInterval = 30000; // 30 seconds
        this.pollTimer = null;
        this.isPolling = false;
        this.lastNotificationId = 0;
        this.maxToasts = 3;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.loadInitialNotifications();
        this.startPolling();
        
        console.log('📱 Notification system initialized');
    }
    
    setupEventListeners() {
        // Handle dropdown show/hide
        const dropdown = document.getElementById('notificationDropdown');
        if (dropdown) {
            dropdown.addEventListener('shown.bs.dropdown', () => {
                this.markVisibleNotificationsAsRead();
            });
        }
        
        // Handle page visibility changes (pause polling when tab not active)
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.stopPolling();
            } else {
                this.startPolling();
                this.pollForUpdates(); // Check immediately when tab becomes active
            }
        });
        
        // Handle window focus (check for updates when user returns)
        window.addEventListener('focus', () => {
            this.pollForUpdates();
        });
    }
    
    loadInitialNotifications() {
        this.showLoading(true);
        
        fetch('/api/notifications/?limit=5', {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json',
            },
            credentials: 'same-origin'
        })
        .then(response => response.json())
        .then(data => {
            this.showLoading(false);
            
            if (data.success) {
                this.updateNotificationBell(data.unread_count);
                this.populateNotificationDropdown(data.notifications);
                
                // Track last notification ID
                if (data.notifications.length > 0) {
                    this.lastNotificationId = Math.max(
                        ...data.notifications.map(n => n.id)
                    );
                }
                
                console.log(`📨 Loaded ${data.notifications.length} notifications`);
            }
        })
        .catch(error => {
            this.showLoading(false);
            console.error('❌ Error loading notifications:', error);
            this.showErrorInDropdown();
        });
    }
    
    startPolling() {
        if (this.isPolling) return;
        
        this.isPolling = true;
        this.pollTimer = setInterval(() => {
            this.pollForUpdates();
        }, this.pollInterval);
        
        console.log('🔄 Started polling for notifications');
    }
    
    stopPolling() {
        this.isPolling = false;
        if (this.pollTimer) {
            clearInterval(this.pollTimer);
            this.pollTimer = null;
        }
        
        console.log('⏸️ Stopped polling');
    }
    
    pollForUpdates() {
        // Only poll if page is visible
        if (document.hidden) return;
        
        fetch(`/api/notifications/?limit=3&since=${this.lastNotificationId}`, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
            credentials: 'same-origin'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success && data.notifications.length > 0) {
                console.log(`🔔 ${data.notifications.length} new notifications received`);
                
                // Show toasts for new notifications
                data.notifications.forEach(notification => {
                    if (notification.id > this.lastNotificationId) {
                        this.showToast(notification);
                    }
                });
                
                // Update UI
                this.updateNotificationBell(data.unread_count);
                this.updateDropdownWithNewNotifications(data.notifications);
                
                // Update last notification ID
                if (data.notifications.length > 0) {
                    this.lastNotificationId = Math.max(
                        this.lastNotificationId,
                        ...data.notifications.map(n => n.id)
                    );
                }
            }
        })
        .catch(error => {
            console.log('⚠️ Polling error (will retry):', error);
        });
    }
    
    updateNotificationBell(unreadCount) {
        const badge = document.getElementById('notification-badge');
        const bell = document.getElementById('notification-bell');
        
        if (badge) {
            badge.textContent = unreadCount || '0';
            badge.style.display = unreadCount > 0 ? 'inline-block' : 'none';
        }
        
        if (bell) {
            if (unreadCount > 0) {
                bell.classList.add('has-notifications');
                bell.classList.add('shake');
                setTimeout(() => bell.classList.remove('shake'), 1000);
            } else {
                bell.classList.remove('has-notifications');
            }
        }
        
        // Update page title with unread count
        this.updatePageTitle(unreadCount);
    }
    
    updatePageTitle(unreadCount) {
        const originalTitle = document.title.replace(/^\(\d+\)\s*/, '');
        document.title = unreadCount > 0 ? `(${unreadCount}) ${originalTitle}` : originalTitle;
    }
    
    populateNotificationDropdown(notifications) {
        const dropdownList = document.getElementById('notification-dropdown-list');
        if (!dropdownList) return;
        
        if (notifications.length === 0) {
            dropdownList.innerHTML = `
                <li class="dropdown-item-text text-center text-muted py-4">
                    <i class="fas fa-bell-slash mb-2" style="font-size: 2rem; opacity: 0.5;"></i>
                    <div>No notifications yet</div>
                </li>
            `;
            return;
        }
        
        dropdownList.innerHTML = notifications.map(notification => 
            this.createNotificationHTML(notification)
        ).join('');
    }
    
    createNotificationHTML(notification) {
        const timeAgo = this.getTimeAgo(notification.created_at);
        const isUnread = !notification.is_read;
        
        return `
            <li>
                <div class="notification-item ${isUnread ? 'unread' : ''}" 
                     data-notification-id="${notification.id}">
                    <div class="d-flex align-items-start">
                        <div class="me-2 mt-1">
                            ${this.getNotificationIcon(notification.type)}
                        </div>
                        <div class="flex-grow-1" onclick="notificationManager.handleNotificationClick(${notification.id}, '${notification.action_url || ''}')">
                            <div class="notification-title small fw-bold mb-1">
                                ${this.escapeHtml(notification.title)}
                            </div>
                            <div class="notification-message small text-muted mb-1">
                                ${this.truncateText(notification.message, 80)}
                            </div>
                            <div class="notification-time tiny text-muted">
                                ${timeAgo}
                            </div>
                        </div>
                        ${isUnread ? '<div class="ms-2"><span class="badge bg-primary rounded-pill">New</span></div>' : ''}
                    </div>
                </div>
            </li>
        `;
    }
    
    getNotificationIcon(type) {
        const icons = {
            'application_update': '<i class="fas fa-file-alt text-primary"></i>',
            'system_announcement': '<i class="fas fa-bullhorn text-info"></i>',
            'reminder': '<i class="fas fa-clock text-warning"></i>',
            'pass_status': '<i class="fas fa-id-card text-success"></i>',
            'alert': '<i class="fas fa-exclamation-triangle text-danger"></i>'
        };
        
        return icons[type] || '<i class="fas fa-info-circle text-secondary"></i>';
    }
    
    showToast(notification) {
        const toastContainer = document.getElementById('toast-container');
        if (!toastContainer) return;
        
        // Remove excess toasts
        const existingToasts = toastContainer.querySelectorAll('.toast');
        if (existingToasts.length >= this.maxToasts) {
            existingToasts[0].remove();
        }
        
        // Create toast
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white ${this.getToastClass(notification.type)} border-0 show`;
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    <div class="fw-bold small">${this.escapeHtml(notification.title)}</div>
                    <div class="small">${this.escapeHtml(notification.message.substring(0, 100))}${notification.message.length > 100 ? '...' : ''}</div>
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" 
                        onclick="this.closest('.toast').remove()"></button>
            </div>
        `;
        
        // Add click handler for action
        if (notification.action_url) {
            toast.style.cursor = 'pointer';
            toast.addEventListener('click', (e) => {
                if (!e.target.classList.contains('btn-close')) {
                    this.markAsRead(notification.id);
                    window.location.href = notification.action_url;
                }
            });
        }
        
        toastContainer.appendChild(toast);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.classList.remove('show');
                setTimeout(() => toast.remove(), 300);
            }
        }, 5000);
        
        console.log(`🍞 Toast shown: ${notification.title}`);
    }
    
    getToastClass(type) {
        const classes = {
            'application_update': 'toast-success',
            'system_announcement': 'toast-info', 
            'reminder': 'toast-warning',
            'alert': 'toast-error'
        };
        
        return classes[type] || 'toast-info';
    }
    
    handleNotificationClick(notificationId, actionUrl) {
        this.markAsRead(notificationId);
        
        if (actionUrl && actionUrl !== 'null' && actionUrl !== '') {
            window.location.href = actionUrl;
        }
        
        // Close dropdown
        const dropdown = bootstrap.Dropdown.getInstance(document.getElementById('notificationDropdown'));
        if (dropdown) dropdown.hide();
    }
    
    markAsRead(notificationId) {
        fetch(`/api/notifications/${notificationId}/mark-read/`, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': this.getCsrfToken(),
                'Content-Type': 'application/json',
            },
            credentials: 'same-origin'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update UI immediately
                const notificationElement = document.querySelector(`[data-notification-id="${notificationId}"]`);
                if (notificationElement) {
                    notificationElement.classList.remove('unread');
                    const badge = notificationElement.querySelector('.badge');
                    if (badge) badge.remove();
                }
                
                // Update bell count
                this.pollForUpdates();
            }
        })
        .catch(error => {
            console.error('Error marking notification as read:', error);
        });
    }
    
    markAllAsRead() {
        fetch('/api/notifications/mark-all-read/', {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': this.getCsrfToken(),
                'Content-Type': 'application/json',
            },
            credentials: 'same-origin'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update UI
                document.querySelectorAll('.notification-item.unread').forEach(item => {
                    item.classList.remove('unread');
                    const badge = item.querySelector('.badge');
                    if (badge) badge.remove();
                });
                
                this.updateNotificationBell(0);
                console.log('✅ All notifications marked as read');
            }
        })
        .catch(error => {
            console.error('Error marking all notifications as read:', error);
        });
    }
    
    // Utility functions
    getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    truncateText(text, maxLength) {
        return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
    }
    
    getTimeAgo(dateString) {
        const now = new Date();
        const date = new Date(dateString);
        const diffInSeconds = Math.floor((now - date) / 1000);
        
        if (diffInSeconds < 60) return 'Just now';
        if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m ago`;
        if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}h ago`;
        
        return `${Math.floor(diffInSeconds / 86400)}d ago`;
    }
    
    showLoading(show) {
        const loading = document.getElementById('notifications-loading');
        if (loading) {
            loading.style.display = show ? 'block' : 'none';
        }
    }
    
    showErrorInDropdown() {
        const dropdownList = document.getElementById('notification-dropdown-list');
        if (dropdownList) {
            dropdownList.innerHTML = `
                <li class="dropdown-item-text text-center text-danger py-3">
                    <i class="fas fa-exclamation-triangle mb-2"></i>
                    <div>Error loading notifications</div>
                    <button class="btn btn-sm btn-outline-danger mt-2" onclick="notificationManager.loadInitialNotifications()">
                        Try Again
                    </button>
                </li>
            `;
        }
    }

    markVisibleNotificationsAsRead() {
    const visibleNotifications = document.querySelectorAll('.notification-item.unread');
    visibleNotifications.forEach(item => {
        const id = item.getAttribute('data-notification-id');
        if (id) {
            this.markAsRead(id);
        }
    });
}
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Only initialize if notification elements exist
    if (document.getElementById('notificationDropdown')) {
        window.notificationManager = new NotificationManager();
    }
});