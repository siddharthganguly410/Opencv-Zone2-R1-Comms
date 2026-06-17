%% ABU Robocon 2026 - "Kung Fu Quest"

% Robot 2 (R2) - Meihua Forest A* Search Solver
% ==============================================================
% Grid layout (1-indexed):
%     1   2   3      <- Entry zone  (row 0)
%     4   5   6
%     7   8   9
%    10  11  12      <- Exit zone   (row 3)
%
% R2 enters from {1,2,3}, exits through {10,11,12}.
%
% A* Algorithm Overview
% --------------------------------------------------------------
% A* finds the OPTIMAL (least-cost) path from a start state to a goal by
% combining two cost measures at every node n:
%
%     f(n) = g(n) + h(n)
%
%   * g(n) : exact cost paid so far to reach n from the start
%   * h(n) : admissible heuristic estimate of remaining cost to goal
%   * f(n) : estimated total cost of the cheapest solution through n
%
% The open-list (min-heap) always expands the node with smallest f(n),
% guaranteeing optimality when h is admissible (never over-estimates).

%% --- MAIN -----------------------------------------------------------

clearvars; clc; close all;

% -- Same config as RL version for direct comparison ---------------
r2_real_scrolls = [2, 7, 9, 11];
fake_scroll     = 5;
r1_scrolls      = [1, 3, 10];

env_config.r2_real = r2_real_scrolls;
env_config.fake    = fake_scroll;
env_config.r1      = r1_scrolls;

fprintf('\n  Forest Configuration:\n');
fprintf('    R2 Real Scrolls : [%s]\n', num2str(r2_real_scrolls));
fprintf('    Fake Scroll     : %d\n', fake_scroll);
fprintf('    R1 Scrolls      : [%s]\n', num2str(r1_scrolls));

% -- Build grid constants ------------------------------------------
ROWS       = 4;
COLS       = 3;
NUM_BLOCKS = 12;
ENTRY_BLOCKS = [1, 2, 3];
EXIT_BLOCKS  = [10, 11, 12];
COST_MOVE    = 1;
COST_COLLECT = 1;

% Build adjacency list (cell array, 1-indexed by block number)
adjacency = cell(NUM_BLOCKS, 1);
for b = 1:NUM_BLOCKS
    [r, c] = block_to_rc(b, COLS);
    nb = [];
    if r > 0,           nb(end+1) = rc_to_block(r-1, c, COLS); end
    if r < ROWS-1,      nb(end+1) = rc_to_block(r+1, c, COLS); end
    if c > 0,           nb(end+1) = rc_to_block(r, c-1, COLS); end
    if c < COLS-1,      nb(end+1) = rc_to_block(r, c+1, COLS); end
    adjacency{b} = nb;
end

% -- 1. Heuristic analysis (pick lowest-h entry) -------------------
h_vals = zeros(1, numel(ENTRY_BLOCKS));
for i = 1:numel(ENTRY_BLOCKS)
    h_vals(i) = heuristic(ENTRY_BLOCKS(i), r2_real_scrolls, EXIT_BLOCKS, COST_COLLECT, COLS);
end
[~, idx]          = min(h_vals);
best_entry_demo   = ENTRY_BLOCKS(idx);
print_heuristic_analysis(best_entry_demo, r2_real_scrolls, EXIT_BLOCKS, COST_COLLECT, COLS);

% -- 2. Detailed single-entry run with full expansion log ----------
t0     = tic;
detail = astar_solve(best_entry_demo, r2_real_scrolls, fake_scroll, ...
                     r1_scrolls, EXIT_BLOCKS, adjacency, ...
                     COST_MOVE, COST_COLLECT, COLS, true, true);
fprintf('  Detailed solve time: %.2f ms\n\n', toc(t0)*1000);

% -- 3. All-entry sweep --------------------------------------------
t1 = tic;
[best, all_res] = solve_all_entries(r2_real_scrolls, fake_scroll, r1_scrolls, ...
                                     ENTRY_BLOCKS, EXIT_BLOCKS, adjacency, ...
                                     COST_MOVE, COST_COLLECT, COLS);
fprintf('\n  All-entries solve time : %.2f ms\n', toc(t1)*1000);
if best.success
    fprintf('  Globally optimal entry : block %d\n', best.entry);
    fprintf('  Globally optimal cost  : %d\n',       best.cost);
else
    fprintf('  No solution found from any entry!\n');
    return;
end

% -- 4. Full path workings -----------------------------------------
print_path_workings(best, env_config);

% -- 5. Plot -------------------------------------------------------
plot_astar(best, all_res, env_config, ENTRY_BLOCKS, EXIT_BLOCKS, ...
           NUM_BLOCKS, ROWS, COLS, 'r2_astar_results.png');

% -- 6. JSON-style summary printed to console ----------------------
fprintf('\n  === SOLUTION SUMMARY (JSON-style) ===\n');
fprintf('  algorithm    : A* Search\n');
fprintf('  heuristic    : admissible NN-tour + Manhattan exit distance\n');
fprintf('  optimal_entry: %d\n', best.entry);
fprintf('  optimal_cost : %d\n', best.cost);
fprintf('  path_steps   : %d\n', numel(best.path));
entries = fieldnames(all_res);
for i = 1:numel(entries)
    e = entries{i};
    r = all_res.(e);
    en = str2double(e(2:end));   % field was stored as 'e1','e2','e3'
    if r.success
        fprintf('  Entry %d: cost=%d  steps=%d  nodes_exp=%d\n', ...
            en, r.cost, numel(r.path), r.nodes_expanded);
    else
        fprintf('  Entry %d: no solution\n', en);
    end
end


%% =================================================================
%  GRID HELPER FUNCTIONS
%% =================================================================

function [r, c] = block_to_rc(b, COLS)
% Convert 1-indexed block number to 0-indexed (row, col).
    r = floor((b - 1) / COLS);
    c = mod((b - 1), COLS);
end

function b = rc_to_block(r, c, COLS)
% Convert 0-indexed (row, col) to 1-indexed block number.
    b = r * COLS + c + 1;
end

function d = manhattan(b1, b2, COLS)
% Manhattan distance between two block numbers.
    [r1, c1] = block_to_rc(b1, COLS);
    [r2, c2] = block_to_rc(b2, COLS);
    d = abs(r1 - r2) + abs(c1 - c2);
end


%% =================================================================
%  HEURISTIC  (admissible)
%% =================================================================

function cost = heuristic(current_block, remaining_scrolls, EXIT_BLOCKS, COST_COLLECT, COLS)
% Admissible h(n) = greedy_scroll_tour_lb + exit_distance_lb.
%
% Never over-estimates because:
%   * Manhattan distance is always <= actual grid steps.
%   * NN-tour cost is a lower bound on any visiting order.

    if isempty(remaining_scrolls)
        % Only need to reach exit
        dists = arrayfun(@(e) manhattan(current_block, e, COLS), EXIT_BLOCKS);
        cost  = min(dists);
        return;
    end

    pos     = current_block;
    visited = false(1, numel(remaining_scrolls));
    cost    = 0;

    while sum(visited) < numel(remaining_scrolls)
        unvisited_idx = find(~visited);
        dists         = arrayfun(@(i) manhattan(pos, remaining_scrolls(i), COLS), ...
                                  unvisited_idx);
        [~, best_i]   = min(dists);
        nearest_idx   = unvisited_idx(best_i);
        nearest_block = remaining_scrolls(nearest_idx);
        cost          = cost + manhattan(pos, nearest_block, COLS) + COST_COLLECT;
        visited(nearest_idx) = true;
        pos = nearest_block;
    end

    % Add distance from last scroll to nearest exit
    exit_dists = arrayfun(@(e) manhattan(pos, e, COLS), EXIT_BLOCKS);
    cost       = cost + min(exit_dists);
end


%% =================================================================
%  A* SOLVER
%% =================================================================

function result = astar_solve(start_block, r2_real_scrolls, fake_scroll, ...
                               r1_scrolls, EXIT_BLOCKS, adjacency, ...
                               COST_MOVE, COST_COLLECT, COLS, verbose, show_expansion)
% A* from start_block: collect all r2_real_scrolls then exit.
%
% Movement through fake/R1 blocks is allowed (cost 1); collecting from
% those blocks is never attempted because they are never in r2_real_scrolls.
%
% Returns a struct with fields:
%   success, path, cost, nodes_expanded, nodes_generated

    scrolls_0 = sort(r2_real_scrolls);
    h0        = heuristic(start_block, scrolls_0, EXIT_BLOCKS, COST_COLLECT, COLS);

    % -- Build first node ----------------------------------------------
    % Each node is a struct:
    %   g, h, f, block, remaining (sorted row vector), path (cell array), id
    global_ctr = 0;
    global_ctr = global_ctr + 1;

    step0.step   = 0;
    step0.block  = start_block;
    step0.action = 'START';
    step0.g      = 0;
    step0.h      = h0;
    step0.f      = h0;
    step0.note   = sprintf('Entry block %d', start_block);

    start_node.g         = 0;
    start_node.h         = h0;
    start_node.f         = h0;
    start_node.block     = start_block;
    start_node.remaining = scrolls_0;
    start_node.path      = {step0};
    start_node.id        = global_ctr;

    % -- Open list as a sorted array of structs (min-heap by f, tie-break g desc) --
    open_list  = {start_node};
    closed_map = containers.Map('KeyType','char','ValueType','double');
    expanded   = 0;
    generated  = 1;

    if verbose
        sep = repmat('=', 1, 68);
        fprintf('\n%s\n', sep);
        fprintf('  A* PATH PLANNING  -  ABU Robocon 2026 R2 Meihua Forest\n');
        fprintf('%s\n', sep);
        fprintf('  Start block      : %d\n', start_block);
        fprintf('  R2 Scrolls       : [%s]\n', num2str(scrolls_0));
        fprintf('  Fake Scroll      : %d  (movement BLOCKED, must route around)\n', fake_scroll);
        fprintf('  R1 Scrolls       : [%s]  (movement OK, collect forbidden)\n', num2str(r1_scrolls));
        fprintf('  h(start)         : %d  <- initial admissible lower bound\n', h0);
        fprintf('  f(start)         : %d  (= g=0 + h=%d)\n', h0, h0);
        fprintf('%s\n\n', sep);
    end

    if show_expansion
        fprintf('  +-- NODE EXPANSION LOG (open-list pops) ----------------+\n');
        fprintf('  |  %4s  %5s  %-16s  %5s  %5s  %5s  Action\n', ...
                '#', 'Block', 'Remaining', 'g', 'h', 'f');
        fprintf('  +-------------------------------------------------------+\n');
    end

    while ~isempty(open_list)
        % Pop node with smallest f (ties broken by largest g, then id)
        [node, open_list] = pop_min(open_list);
        expanded = expanded + 1;

        state_key = make_key(node.block, node.remaining);

        % Skip if we already found a cheaper route to this state
        if isKey(closed_map, state_key) && closed_map(state_key) <= node.g
            continue;
        end
        closed_map(state_key) = node.g;

        if show_expansion
            if isempty(node.remaining)
                rem_str = '[ done ]';
            else
                rem_str = sprintf('[%s]', strtrim(num2str(node.remaining)));
            end
            last_act = node.path{end}.action;
            fprintf('  |  %4d  [%2d]  %-16s  %5d  %5d  %5d  %s\n', ...
                expanded, node.block, rem_str, node.g, node.h, node.f, last_act);
        end

        % -- GOAL CHECK ---------------------------------------------
        if isempty(node.remaining) && ismember(node.block, EXIT_BLOCKS)
            if show_expansion
                fprintf('  +-------- GOAL REACHED --------------------------------+\n');
            end
            if verbose
                fprintf('\n  Optimal solution found!\n');
                fprintf('    Nodes expanded  : %d\n', expanded);
                fprintf('    Nodes generated : %d\n', generated);
                fprintf('    Optimal cost g  : %d\n', node.g);
                fprintf('    Path steps      : %d\n\n', numel(node.path));
            end
            result.success         = true;
            result.path            = node.path;
            result.cost            = node.g;
            result.nodes_expanded  = expanded;
            result.nodes_generated = generated;
            return;
        end

        % -- EXPAND: move to neighbours ------------------------------
        for nb = adjacency{node.block}
            % LOGIC FIX: robot CANNOT enter the fake-scroll block
            if nb == fake_scroll
                continue;
            end
            new_g = node.g + COST_MOVE;
            note  = sprintf('Move -> %d', nb);
            if ismember(nb, r1_scrolls), note = [note ' (R1 scroll block)'];      end

            new_rem  = node.remaining;
            new_h    = heuristic(nb, new_rem, EXIT_BLOCKS, COST_COLLECT, COLS);
            step_new = make_step(numel(node.path), nb, ...
                                 sprintf('MOVE -> %d', nb), new_g, new_h, note);

            global_ctr = global_ctr + 1;
            new_node   = make_node(new_g, new_h, nb, new_rem, ...
                                   [node.path, {step_new}], global_ctr);
            generated  = generated + 1;
            nk         = make_key(nb, new_rem);
            if ~isKey(closed_map, nk) || closed_map(nk) > new_g
                open_list = insert_node(open_list, new_node);
            end
        end

        % -- EXPAND: collect (only if standing on own real scroll) --
        if ismember(node.block, node.remaining)
            new_rem = node.remaining(node.remaining ~= node.block);
            new_g   = node.g + COST_COLLECT;
            new_h   = heuristic(node.block, new_rem, EXIT_BLOCKS, COST_COLLECT, COLS);
            note    = sprintf('Collect scroll at block %d', node.block);
            if isempty(new_rem), note = [note '  <- ALL SCROLLS COLLECTED']; end
            step_new = make_step(numel(node.path), node.block, ...
                                  sprintf('COLLECT @ %d', node.block), new_g, new_h, note);

            global_ctr = global_ctr + 1;
            new_node   = make_node(new_g, new_h, node.block, new_rem, ...
                                   [node.path, {step_new}], global_ctr);
            generated  = generated + 1;
            nk         = make_key(node.block, new_rem);
            if ~isKey(closed_map, nk) || closed_map(nk) > new_g
                open_list = insert_node(open_list, new_node);
            end
        end
    end

    fprintf('  Open list exhausted - no solution from this entry.\n');
    result.success         = false;
    result.nodes_expanded  = expanded;
    result.nodes_generated = generated;
end


%% =================================================================
%  SOLVE FROM ALL ENTRIES
%% =================================================================

function [best, all_res] = solve_all_entries(r2_real_scrolls, fake_scroll, r1_scrolls, ...
                                              ENTRY_BLOCKS, EXIT_BLOCKS, adjacency, ...
                                              COST_MOVE, COST_COLLECT, COLS)
    best    = struct('success', false);
    all_res = struct();
    sep     = repmat('=', 1, 68);
    fprintf('\n%s\n', sep);
    fprintf('  ALL-ENTRY SWEEP  (finding globally optimal start)\n');
    fprintf('%s\n\n', sep);

    for entry = sort(ENTRY_BLOCKS)
        res = astar_solve(entry, r2_real_scrolls, fake_scroll, r1_scrolls, ...
                          EXIT_BLOCKS, adjacency, COST_MOVE, COST_COLLECT, COLS, ...
                          false, false);
        fld = sprintf('e%d', entry);
        all_res.(fld) = res;
        if res.success
            fprintf('  Entry %d: cost=%d  steps=%d  nodes_exp=%d\n', ...
                    entry, res.cost, numel(res.path), res.nodes_expanded);
            if ~best.success || res.cost < best.cost
                best       = res;
                best.entry = entry;
            end
        else
            fprintf('  Entry %d: no solution\n', entry);
        end
    end
end


%% =================================================================
%  HEURISTIC ANALYSIS PRINTER
%% =================================================================

function print_heuristic_analysis(start_block, r2_real_scrolls, EXIT_BLOCKS, COST_COLLECT, COLS)
    remaining = sort(r2_real_scrolls);
    h_val     = heuristic(start_block, remaining, EXIT_BLOCKS, COST_COLLECT, COLS);
    sep       = repmat('-', 1, 62);

    fprintf('\n%s\n', sep);
    fprintf('  HEURISTIC ANALYSIS  h(start=block %d)\n', start_block);
    fprintf('%s\n', sep);
    fprintf('  Uncollected scrolls: [%s]\n', num2str(remaining));
    fprintf('\n  -- Step 1: Greedy nearest-neighbour scroll tour --\n');

    pos     = start_block;
    visited = false(1, numel(remaining));
    total   = 0;
    while sum(visited) < numel(remaining)
        unv   = find(~visited);
        dists = arrayfun(@(i) manhattan(pos, remaining(i), COLS), unv);
        [d, bi] = min(dists);
        nearest = remaining(unv(bi));
        c       = d + COST_COLLECT;
        total   = total + c;
        fprintf('    Block %2d -> Block %2d  Manhattan=%d  +collect=%d  subtotal=%d\n', ...
                pos, nearest, d, COST_COLLECT, c);
        visited(unv(bi)) = true;
        pos = nearest;
    end

    exit_dists   = arrayfun(@(e) manhattan(pos, e, COLS), EXIT_BLOCKS);
    [exit_d, ei] = min(exit_dists);
    nearest_exit = EXIT_BLOCKS(ei);
    fprintf('\n  -- Step 2: Exit distance from last scroll --\n');
    fprintf('    Block %2d -> Exit %2d  Manhattan=%d\n', pos, nearest_exit, exit_d);
    fprintf('\n  h(start=%d) = scroll_tour(%d) + exit(%d) = %d\n', ...
            start_block, total, exit_d, h_val);
    fprintf('  Admissible: h<=true cost (Manhattan LB on 4x3 grid)\n');
    fprintf('%s\n\n', sep);
end


%% =================================================================
%  PATH WORKINGS PRINTER
%% =================================================================

function print_path_workings(result, env_config)
    EXIT_BLOCKS = [10, 11, 12];
    if ~result.success
        fprintf('  No solution.\n\n');
        return;
    end
    path = result.path;
    r2   = env_config.r2_real;
    fake = env_config.fake;
    r1   = env_config.r1;
    W    = 76;
    sep  = repmat('=', 1, W);
    dsh  = repmat('-', 1, W);

    fprintf('\n%s\n', sep);
    fprintf('  FULL A* PATH WORKINGS  (entry=%d  cost=%d  steps=%d)\n', ...
            result.entry, result.cost, numel(path));
    fprintf('%s\n', sep);
    fprintf('  %4s  %5s  %6s  %6s  %6s  Action / Note\n', ...
            'Step', 'Block', 'g', 'h', 'f');
    fprintf('%s\n', dsh);

    collected = [];
    for i = 1:numel(path)
        s   = path{i};
        blk = s.block;
        tags = '';
        if ismember(blk, r2) && ~ismember(blk, collected)
            tags = [tags ' [R2 scroll here]'];
        end
        if blk == fake,        tags = [tags ' [! fake]']; end
        if ismember(blk, r1),  tags = [tags ' [R1]'];     end
        if contains(s.action, 'COLLECT')
            collected(end+1) = blk;
            tags = [tags sprintf(' [v %d/%d collected]', numel(collected), numel(r2))];
        end
        if ismember(blk, EXIT_BLOCKS), tags = [tags ' [EXIT ZONE]']; end
        fprintf('  %4d  [%2d]  %6d  %6d  %6d  %s%s\n', ...
                s.step, blk, s.g, s.h, s.f, s.action, tags);
    end
    fprintf('%s\n', dsh);
    fprintf('  Optimal cost   : %d  (move=1, collect=1)\n', result.cost);
    fprintf('  Nodes expanded : %d\n', result.nodes_expanded);
    fprintf('  Nodes generated: %d\n', result.nodes_generated);
    fprintf('%s\n\n', sep);
end


%% =================================================================
%  PLOT DASHBOARD  –  two-panel layout matching reference image
%% =================================================================

function plot_astar(result, all_res, env_cfg, ENTRY_BLOCKS, EXIT_BLOCKS, ...
                    NUM_BLOCKS, ROWS, COLS, save_path)

    % ------------------------------------------------------------------
    % Colour palette  (dark-navy theme matching reference image)
    % ------------------------------------------------------------------
    FIGBG   = [0.059 0.067 0.090];          % near-black figure background
    BG      = [0.102 0.114 0.180];          % panel background (dark navy)
    TEXT    = [0.878 0.878 0.878];          % default text
    ACCENT  = [0.000 0.898 1.000];          % cyan  (entry labels, badges)
    SUCCESS = [0.412 1.000 0.278];          % green (arrows, exit label)
    SCROLL  = [1.000 0.780 0.000];          % golden-yellow  – R2 scroll
    FAKE    = [0.941 0.302 0.494];          % pink-red        – fake scroll
    R1C     = [0.600 0.490 0.620];          % muted purple    – R1 scroll
    EMPTY   = [0.145 0.161 0.255];          % dark slate      – empty block
    BORDER  = [0.000 0.820 0.900];          % cyan outer grid border

    % ------------------------------------------------------------------
    % Figure:  wide 2-panel window
    % ------------------------------------------------------------------
    fig = figure('Color', FIGBG, 'Position', [40 60 1100 560]);
    sgtitle('ABU Robocon 2026 – R2  |  A* Optimal Path Planning', ...
            'Color', 'white', 'FontSize', 13, 'FontWeight', 'bold', ...
            'FontName', 'Monospaced');

    % ------------------------------------------------------------------
    % Grid geometry constants (shared by both panels)
    % ------------------------------------------------------------------
    SZ   = 1.00;    % cell square size  (data units)
    GAP  = 0.10;    % gap between adjacent cells
    PAD  = 0.10;    % half-inset so rounded corners don't touch borders

    total_w = COLS * SZ + (COLS-1) * GAP;
    total_h = ROWS * SZ + (ROWS-1) * GAP;

    xl = [-0.50, total_w + 0.30];
    yl = [-1.20, total_h + 0.30];

    % Centre helpers ---------------------------------------------------
    blk_cx = @(c_) c_*(SZ+GAP) + SZ*0.50;
    blk_cy = @(r_) (ROWS-1-r_)*(SZ+GAP) + SZ*0.50;

    % ------------------------------------------------------------------
    % Helper: draw_rounded_rect
    % ------------------------------------------------------------------
    function draw_rounded_rect(ax, x, y, w, h, r, fc, ec, lw)
        r = min(r, min(w,h)*0.48);
        theta = linspace(0, pi/2, 16);
        CX = [x+r, x+w-r, x+w-r, x+r];
        CY = [y+r, y+r,   y+h-r, y+h-r];
        px = []; py = [];
        for qi = 1:4
            angs = (qi-1)*pi/2 + theta;
            px = [px, CX(qi) + r*cos(angs)]; %#ok<AGROW>
            py = [py, CY(qi) + r*sin(angs)]; %#ok<AGROW>
        end
        patch(ax, px, py, fc, 'EdgeColor', ec, 'LineWidth', lw, 'FaceAlpha', 1.0);
    end

    % ------------------------------------------------------------------
    % Helper: draw outer grid border (thick cyan rectangle around grid)
    % ------------------------------------------------------------------
    function draw_outer_border(ax)
        brd = 0.08;
        bx  = -brd;
        by  = -brd;
        bw  = total_w + 2*brd;
        bh  = total_h + 2*brd;
        rectangle(ax, 'Position', [bx by bw bh], ...
                  'EdgeColor', BORDER, 'LineWidth', 3.0, 'FaceColor', 'none', ...
                  'Curvature', 0.03);
    end

    % ------------------------------------------------------------------
    % Helper: draw_forest(ax, show_path_steps, ttl)
    %   show_path_steps = false  → plain forest layout
    %   show_path_steps = true   → overlays step-number badges + arrows
    % ------------------------------------------------------------------
    function draw_forest(ax, show_path_steps, ttl)
        set(ax, 'Color', BG, 'XLim', xl, 'YLim', yl);
        axis(ax, 'equal'); axis(ax, 'off');
        title(ax, ttl, 'Color', TEXT, 'FontSize', 10.5, 'FontWeight', 'bold');
        hold(ax, 'on');

        draw_outer_border(ax);

        for b = 1:NUM_BLOCKS
            [row, col] = block_to_rc(b, COLS);
            cx0 = col*(SZ+GAP);
            cy0 = (ROWS-1-row)*(SZ+GAP);

            % Block fill colour
            if ismember(b, env_cfg.r2_real),  fc = SCROLL;
            elseif b == env_cfg.fake,          fc = FAKE;
            elseif ismember(b, env_cfg.r1),    fc = R1C;
            else,                              fc = EMPTY;
            end

            % Block border  (slightly lighter than background)
            ec = [0.22 0.24 0.36]; lw = 1.0;

            bx = cx0 + PAD/2;
            by = cy0 + PAD/2;
            bw = SZ  - PAD;
            bh = SZ  - PAD;
            draw_rounded_rect(ax, bx, by, bw, bh, 0.12, fc, ec, lw);

            % Block number  (large, white, top-centre)
            text(ax, cx0+SZ*0.50, cy0+SZ*0.68, num2str(b), ...
                 'HorizontalAlignment','center','VerticalAlignment','middle', ...
                 'FontSize', 11, 'FontWeight','bold', 'Color','white');

            % Sub-label  (icon, bottom-centre)
            if ismember(b, env_cfg.r2_real),  sym = char(9633);   % □
            elseif b == env_cfg.fake,          sym = char(9651);   % △
            elseif ismember(b, env_cfg.r1),    sym = 'R1';
            else,                              sym = '';
            end
            if ~isempty(sym)
                text(ax, cx0+SZ*0.50, cy0+SZ*0.26, sym, ...
                     'HorizontalAlignment','center','VerticalAlignment','middle', ...
                     'FontSize', 8, 'Color', 'white');
            end
        end

        % ENTRY / EXIT zone labels on the left
        entry_y = (ROWS-1)*(SZ+GAP) + SZ*0.50;
        exit_y  =          0*(SZ+GAP) + SZ*0.50;
        text(ax, -0.12, entry_y, 'ENTRY', ...
             'HorizontalAlignment','right','VerticalAlignment','middle', ...
             'FontSize', 7.5, 'Color', ACCENT, 'FontAngle','italic','FontWeight','bold');
        text(ax, -0.12, exit_y, 'EXIT', ...
             'HorizontalAlignment','right','VerticalAlignment','middle', ...
             'FontSize', 7.5, 'Color', SUCCESS, 'FontAngle','italic','FontWeight','bold');

        % ------ Legend (bottom of forest layout panel only) -----------
        if ~show_path_steps
            leg_items = {SCROLL, 'R2 Scroll'; FAKE, 'Fake (avoid collect)'; ...
                         R1C, 'R1 Scroll'; EMPTY, 'Empty'};
            lsw  = 0.24; lsh = 0.13; lgap = 0.20;
            lx0  = 0.00; ly0 = -1.16;
            n_leg = size(leg_items,1);
            leg_bg_h = n_leg*lgap + 0.04;
            leg_bg_w = 1.40;
            fill(ax, lx0 + [-0.06 leg_bg_w leg_bg_w -0.06 -0.06], ...
                     ly0 + [-0.04 -0.04 leg_bg_h leg_bg_h -0.04], ...
                     [0.09 0.10 0.16], 'EdgeColor', [0.28 0.30 0.42], 'LineWidth', 0.7);
            for li = 1:n_leg
                ly = ly0 + (n_leg-li)*lgap;
                fill(ax, lx0 + [0 lsw lsw 0 0], ly + [0 0 lsh lsh 0], ...
                     leg_items{li,1}, 'EdgeColor', [0.45 0.46 0.52], 'LineWidth', 0.6);
                text(ax, lx0+lsw+0.08, ly+lsh*0.50, leg_items{li,2}, ...
                     'VerticalAlignment','middle','FontSize', 7.5, 'Color', TEXT);
            end
        end

        % ------ Path overlays (badges + arrows) -----------------------
        if show_path_steps && result.success
            path = result.path;

            % Build step-list per unique block
            step_map = containers.Map('KeyType','int32','ValueType','any');
            for i = 1:numel(path)
                b = path{i}.block;
                if isKey(step_map, int32(b))
                    step_map(int32(b)) = [step_map(int32(b)), path{i}.step];
                else
                    step_map(int32(b)) = path{i}.step;
                end
            end

            % Cyan badge with step numbers
            keys_list = keys(step_map);
            for ki = 1:numel(keys_list)
                b = keys_list{ki};
                steps = step_map(b);
                [row, col] = block_to_rc(b, COLS);
                % Show up to 2 step numbers; comma-separated
                lbl = ['#' strjoin(arrayfun(@num2str, steps(1:min(2,end)), ...
                                   'UniformOutput', false), ',')];
                text(ax, blk_cx(col), blk_cy(row), lbl, ...
                     'HorizontalAlignment','center','VerticalAlignment','middle', ...
                     'FontSize', 7, 'Color', [0.02 0.02 0.02], ...
                     'FontWeight','bold', ...
                     'BackgroundColor', ACCENT, ...
                     'EdgeColor', [0 0.6 0.7], ...
                     'LineWidth', 0.8, ...
                     'Margin', 2.0);
            end

            % Green arrows between consecutive distinct blocks
            prev = -1;
            for i = 1:numel(path)
                b = path{i}.block;
                if prev > 0 && prev ~= b
                    [r1p, c1p] = block_to_rc(prev, COLS);
                    [r2p, c2p] = block_to_rc(b, COLS);
                    x1 = blk_cx(c1p); y1 = blk_cy(r1p);
                    x2 = blk_cx(c2p); y2 = blk_cy(r2p);
                    dx = x2-x1; dy = y2-y1;
                    len = sqrt(dx^2+dy^2);
                    off = 0.30;
                    quiver(ax, x1 + off*dx/len, y1 + off*dy/len, ...
                           (len-2*off)*dx/len, (len-2*off)*dy/len, ...
                           0, 'Color', SUCCESS, 'LineWidth', 2.2, ...
                           'MaxHeadSize', 1.0, 'AutoScale', 'off');
                end
                prev = b;
            end

            % Caption bar at the very bottom of the panel
            caption = sprintf('Entry %d  |  Cost=%d  |  Steps=%d', ...
                              result.entry, result.cost, numel(path));
            text(ax, total_w*0.50, yl(1)+0.10, caption, ...
                 'HorizontalAlignment','center','VerticalAlignment','bottom', ...
                 'FontSize', 8.5, 'Color', ACCENT, 'FontWeight','bold');
        end

        hold(ax,'off');
    end

    % ------------------------------------------------------------------
    % Panel 1 – Forest Layout  (left half)
    % ------------------------------------------------------------------
    ax0 = subplot(1, 2, 1, 'Parent', fig);
    draw_forest(ax0, false, 'Forest Layout');

    % ------------------------------------------------------------------
    % Panel 2 – A* Optimal Path  (right half)
    % ------------------------------------------------------------------
    ax1 = subplot(1, 2, 2, 'Parent', fig);
    draw_forest(ax1, true, 'A* Optimal Path');

    % ------------------------------------------------------------------
    % Tighten spacing so panels fill the figure nicely
    % ------------------------------------------------------------------
    set(fig, 'Units', 'normalized');
    ax0.Position = [0.03  0.05  0.44  0.86];
    ax1.Position = [0.52  0.05  0.44  0.86];

    % ------------------------------------------------------------------
    % Save
    % ------------------------------------------------------------------
    exportgraphics(fig, save_path, 'Resolution', 150, 'BackgroundColor', FIGBG);
    fprintf('  Plot saved -> %s\n', save_path);
end


%% =================================================================
%  OPEN-LIST HELPERS  (sorted insertion, sorted pop)
%% =================================================================

function n = make_node(g, h, block, remaining, path, id)
    n.g         = g;
    n.h         = h;
    n.f         = g + h;
    n.block     = block;
    n.remaining = remaining;
    n.path      = path;
    n.id        = id;
end

function s = make_step(step_idx, block, action, g, h, note)
    s.step   = step_idx;
    s.block  = block;
    s.action = action;
    s.g      = g;
    s.h      = h;
    s.f      = g + h;
    s.note   = note;
end

function k = make_key(block, remaining)
% Deterministic string key for (block, remaining_scrolls).
    k = sprintf('%d|%s', block, num2str(sort(remaining)));
end

function open_list = insert_node(open_list, node)
% Insert node into open_list maintaining sort order:
%   primary   : smallest f
%   secondary : largest g  (prefer deeper nodes)
%   tertiary  : smallest id (insertion order)
    open_list{end+1} = node;
    n = numel(open_list);
    if n == 1, return; end
    % Bubble the new element into sorted position (insertion sort on last)
    i = n;
    while i > 1
        a = open_list{i-1};
        b = open_list{i};
        if lt_node(b, a)
            open_list{i-1} = b;
            open_list{i}   = a;
            i = i - 1;
        else
            break;
        end
    end
end

function result = lt_node(a, b)
% Return true if node a should be expanded before node b.
    if a.f ~= b.f,    result = a.f < b.f;   return; end
    if a.g ~= b.g,    result = a.g > b.g;   return; end  % prefer deeper
    result = a.id < b.id;
end

function [node, open_list] = pop_min(open_list)
% Pop the first (minimum) element from the sorted open list.
    node      = open_list{1};
    open_list = open_list(2:end);
end