/* Leaderboard Filtering, Column Selection, and Sorting */

document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchInput');
    const columnChips = document.querySelectorAll('#columnChips .chip');
    const typeChips = document.querySelectorAll('#typeChips .chip');
    const precisionChips = document.querySelectorAll('#precisionChips .chip');
    const table = document.querySelector('.table-shell table');
    const headerCells = table.querySelectorAll('thead th');
    const tbody = table.querySelector('tbody');
    let rows = Array.from(tbody.querySelectorAll('tr[data-model-type]'));
    let noResultsRow = tbody.querySelector('tr[data-placeholder]');

    let currentSortColumn = 'Average';
    let currentSortDirection = 'desc'; // 'asc' or 'desc'

    // Add sort arrows to headers
    headerCells.forEach(th => {
        const arrow = document.createElement('span');
        arrow.className = 'sort-arrow';
        arrow.innerHTML = '▼'; // Default desc arrow
        if (th.dataset.column === currentSortColumn) {
            arrow.classList.add('active');
        }
        th.appendChild(arrow);
        th.addEventListener('click', () => handleSort(th.dataset.column));
    });

    function handleSort(columnName) {
        if (!columnName) return;

        if (currentSortColumn === columnName) {
            currentSortDirection = currentSortDirection === 'asc' ? 'desc' : 'asc';
        } else {
            currentSortColumn = columnName;
            currentSortDirection = 'desc'; // Default to desc for new column
        }

        // Update arrows
        headerCells.forEach(th => {
            const arrow = th.querySelector('.sort-arrow');
            if (arrow) {
                arrow.classList.toggle('active', th.dataset.column === currentSortColumn);
                if (th.dataset.column === currentSortColumn) {
                    arrow.innerHTML = currentSortDirection === 'asc' ? '▲' : '▼';
                } else {
                    arrow.innerHTML = '▼'; // Reset others
                }
            }
        });

        sortRows();
        updateTableDisplay();
    }

    function sortRows() {
        rows.sort((a, b) => {
            let valA = a.querySelector(`td[data-column="${currentSortColumn}"]`).textContent.trim();
            let valB = b.querySelector(`td[data-column="${currentSortColumn}"]`).textContent.trim();

            // Try to parse as numbers for sorting
            const numA = parseFloat(valA);
            const numB = parseFloat(valB);

            if (!isNaN(numA) && !isNaN(numB)) {
                return currentSortDirection === 'asc' ? numA - numB : numB - numA;
            }

            // Fallback to string comparison
            return currentSortDirection === 'asc' 
                ? valA.localeCompare(valB) 
                : valB.localeCompare(valA);
        });

        // Re-append rows in sorted order
        rows.forEach(row => tbody.appendChild(row));
        if (noResultsRow) tbody.appendChild(noResultsRow);
    }

    function getSelectedValues(chips, dataKey) {
        return Array.from(chips)
            .filter(chip => chip.classList.contains('checked') && !chip.classList.contains('locked'))
            .map(chip => (dataKey === 'column' ? chip.dataset.column.trim() : chip.dataset.value.trim()));
    }

    function updateColumns(visibleColumns) {
        headerCells.forEach(cell => {
            const columnName = cell.dataset.column;
            if (!columnName || columnName === 'Model') return;
            cell.style.display = visibleColumns.includes(columnName) ? '' : 'none';
        });

        rows.forEach(row => {
            row.querySelectorAll('td[data-column]').forEach(cell => {
                if (cell.dataset.column === 'Model') return;
                cell.style.display = visibleColumns.includes(cell.dataset.column) ? '' : 'none';
            });
        });

        if (noResultsRow && visibleColumns.length > 0) {
            noResultsRow.querySelector('td').colSpan = 1 + visibleColumns.length;
        }
    }

    function updateTableDisplay() {
        const visibleColumns = getSelectedValues(columnChips, 'column');
        const selectedTypes = getSelectedValues(typeChips, 'value');
        const selectedPrecisions = getSelectedValues(precisionChips, 'value');
        const searchTerms = searchInput.value
            .toLowerCase()
            .split(';')
            .map(term => term.trim())
            .filter(Boolean);

        const defaultColumns = ['Average', 'Non-toxicity', 'Non-Stereotype', 'OoD', 'Privacy', 'Ethics', 'Fairness', 'Type', 'Architecture', 'Precision', '#Params (B)'];
        updateColumns(visibleColumns.length ? visibleColumns : defaultColumns);

        if (rows.length === 0) {
            if (noResultsRow) {
                noResultsRow.style.display = '';
                noResultsRow.querySelector('td').textContent = 'No model to show';
            }
            return;
        }

        let anyRowVisible = false;
        rows.forEach(row => {
            const modelCell = row.querySelector('td[data-column="Model"]');
            if (!modelCell) return;

            const model = modelCell.textContent.toLowerCase();
            const modelType = row.dataset.modelType.toLowerCase();
            const precision = row.dataset.precision.toLowerCase();

            const matchesType = !selectedTypes.length || selectedTypes.includes(modelType);
            const matchesPrecision = !selectedPrecisions.length || selectedPrecisions.includes(precision);
            const matchesSearch = !searchTerms.length || searchTerms.some(term => model.includes(term) || modelType.includes(term) || precision.includes(term));
            const visible = matchesType && matchesPrecision && matchesSearch;

            row.style.display = visible ? '' : 'none';
            if (visible) anyRowVisible = true;
        });

        if (!anyRowVisible && noResultsRow) {
            noResultsRow.style.display = '';
            noResultsRow.querySelector('td').textContent = 'No model to show';
        } else if (noResultsRow) {
            noResultsRow.style.display = 'none';
        }
    }

    function toggleChip(event) {
        const chip = event.currentTarget;
        if (chip.classList.contains('locked')) return;
        chip.classList.toggle('checked');
        updateTableDisplay();
    }

    // Event listeners
    columnChips.forEach(chip => chip.addEventListener('click', toggleChip));
    typeChips.forEach(chip => chip.addEventListener('click', toggleChip));
    precisionChips.forEach(chip => chip.addEventListener('click', toggleChip));
    searchInput.addEventListener('input', updateTableDisplay);
    searchInput.addEventListener('keydown', event => {
        if (event.key === 'Enter') {
            event.preventDefault();
            updateTableDisplay();
        }
    });

    // Initial display and sort
    sortRows();
    updateTableDisplay();
});
