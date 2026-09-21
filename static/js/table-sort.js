document.addEventListener('DOMContentLoaded', () => {
    const sortableHeaders = document.querySelectorAll('th.sortable');
    
    // Store original index for rows for default state
    document.querySelectorAll('table.data-table tbody').forEach(tbody => {
        Array.from(tbody.querySelectorAll('tr')).forEach((row, index) => {
            row.dataset.originalIndex = index;
        });
    });

    sortableHeaders.forEach(th => {
        // Initialize sort state
        th.dataset.sortState = 'none';
        
        th.addEventListener('click', () => {
            const table = th.closest('table');
            const tbody = table.querySelector('tbody');
            if (!tbody) return;
            const rows = Array.from(tbody.querySelectorAll('tr'));
            if (rows.length === 0) return;
            
            const colIndex = Array.from(th.parentNode.children).indexOf(th);
            const type = th.dataset.type || 'text';
            
            let currentState = th.dataset.sortState;
            let nextState = 'asc';
            if (currentState === 'none') nextState = 'asc';
            else if (currentState === 'asc') nextState = 'desc';
            else if (currentState === 'desc') nextState = 'none';
            
            // Reset all other headers in the table
            sortableHeaders.forEach(header => {
                if (header.closest('table') === table) {
                    header.dataset.sortState = 'none';
                    updateSortIcon(header, 'none');
                }
            });
            
            th.dataset.sortState = nextState;
            updateSortIcon(th, nextState);
            
            if (nextState === 'none') {
                rows.sort((a, b) => {
                    return a.dataset.originalIndex - b.dataset.originalIndex;
                });
            } else {
                rows.sort((a, b) => {
                    let aVal = a.children[colIndex].textContent.trim();
                    let bVal = b.children[colIndex].textContent.trim();
                    
                    if (type === 'numeric') {
                        let aNum = parseFloat(aVal) || 0;
                        let bNum = parseFloat(bVal) || 0;
                        return nextState === 'asc' ? aNum - bNum : bNum - aNum;
                    } else if (type === 'date') {
                        let dateA = new Date(aVal).getTime() || 0;
                        let dateB = new Date(bVal).getTime() || 0;
                        return nextState === 'asc' ? dateA - dateB : dateB - dateA;
                    } else {
                        return nextState === 'asc' ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
                    }
                });
            }
            
            // Re-append rows
            rows.forEach(row => tbody.appendChild(row));
        });
    });
    
    function updateSortIcon(th, state) {
        const container = th.querySelector('.sort-icon-container');
        if (!container) return;
        let iconName = 'arrow-up-down';
        if (state === 'asc') iconName = 'arrow-up';
        if (state === 'desc') iconName = 'arrow-down';
        
        container.innerHTML = `<i data-lucide="${iconName}" class="sort-icon"></i>`;
        if (window.lucide) {
            lucide.createIcons();
        }
    }
});
