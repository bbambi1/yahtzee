function isSorted(m) {
    for[i in 0..3] {
        if(m[i] > m[i+1]) return false;
    }
    return true;
}

function sorted(m) {
    local r = {};
    for[k,v in m] r[k] = v;
    size = r.count();
    for[i in 0..size-1] {
        for[j in 0..size-1] {
            if(r[i] < r[j]) {
                t = r[i];
                r[i] = r[j];
                r[j] = t;
            }
        }
    }
    return r;
}

function createHand(d1, d2, d3, d4, d5) {
    local hand = map(d1, d2, d3, d4, d5);
    if(!isSorted(hand)) throw "hand is not sorted";
    return hand;
}

function handToId(hand) {
    local id = 0;
    for[v in hand.values()] id = 6*id + (v-1);
    return id;
}

function handFromId(id) {
    local hand = {};
    hand[4] = id % 6 + 1;
    id = floor(id / 6);
    hand[3] = id % 6 + 1;
    id = floor(id / 6);
    hand[2] = id % 6 + 1;
    id = floor(id / 6);
    hand[1] = id % 6 + 1;
    id = floor(id / 6);
    hand[0] = id % 6 + 1;
    return hand;
}

function all_squares() {
    return {
        "Ones",
        "Twos",
        "Threes",
        "Fours",
        "Fives",
        "Sixes",
        "3_of_a_Kind",
        "4_of_a_Kind",
        "Full_House",
        "Small_Straight",
        "Large_Straight",
        "Yahtzee",
        "Chance"
    };
}

function eval(hand) {
    if(hand.count() != 5) throw "hand not of size 5";
    if(!isSorted(hand)) throw "hand must be sorted";
    local e;
    e["Ones"] = sum[v in hand.values()](v == 1) * 1;
    e["Twos"] = sum[v in hand.values()](v == 2) * 2;
    e["Threes"] = sum[v in hand.values()](v == 3) * 3;
    e["Fours"] = sum[v in hand.values()](v == 4) * 4;
    e["Fives"] = sum[v in hand.values()](v == 5) * 5;
    e["Sixes"] = sum[v in hand.values()](v == 6) * 6;
    e["3_of_a_Kind"] = max(3*hand[0]*(hand[0] == hand[2]),
                           3*hand[1]*(hand[1] == hand[3]),
                           3*hand[2]*(hand[2] == hand[4]));
    e["4_of_a_Kind"] = max(4*hand[0]*(hand[0] == hand[3]),
                           4*hand[1]*(hand[1] == hand[4]));
    e["Full_House"] = 25*or(hand[0] == hand[1] && hand[2] == hand[4],
                         hand[0] == hand[2] && hand[3] == hand[4]);
    e["Small_Straight"] = 30*or(hand[0]+1 == hand[1] && hand[1]+1 == hand[2] && hand[2]+1 == hand[3],
                             hand[1]+1 == hand[2] && hand[2]+1 == hand[3] && hand[3]+1 == hand[4]);
    e["Large_Straight"] = 40*(hand[0]+1 == hand[1] && hand[1]+1 == hand[2] && hand[2]+1 == hand[3] && hand[3]+1 == hand[4]);
    e["Yahtzee"] = 50*(hand[0] == hand[4]);
    e["Chance"] = sum[v in hand.values()](v);
    return e;
}

function createHands() {
    local hands = {};
    for[k in 0..6*6*6*6*6-1] {
        local d = k;
        local d1 = (d % 6) + 1;
        d = floor(d/6);
        local d2 = (d % 6) + 1;
        if(!(d2 >= d1)) continue;
        d = floor(d/6);
        local d3 = (d % 6) + 1;
        if(!(d3 >= d2)) continue;
        d = floor(d/6);
        local d4 = (d % 6) + 1;
        if(!(d4 >= d3)) continue;
        d = floor(d/6);
        local d5 = (d % 6) + 1;
        if(!(d5 >= d4)) continue;
        local hand = createHand(d1, d2, d3, d4, d5);
        local id = handToId(hand);
        hands[id] = hand;
    }
    return hands;
}

function createRethrow(r1, r2, r3, r4, r5) {
    local rt = { r1, r2, r3, r4, r5 };
    return rt;
}

function rethrowToId(rt) {
    local id = 0;
    for[v in rt.values()] id = 2*id + v;
    return id;
}

function rethrowFromId(id) {
    local rt = {};
    rt[4] = id % 2;
    id = floor(id / 2);
    rt[3] = id % 2;
    id = floor(id / 2);
    rt[2] = id % 2;
    id = floor(id / 2);
    rt[1] = id % 2;
    id = floor(id / 2);
    rt[0] = id % 2;
    return rt;
}

function createRethrows() {
    local rethrows = {};
    for[k in 0..2*2*2*2*2-1] {
        local rt = rethrowFromId(k);
        local id = rethrowToId(rt);
        if(id != k) throw "rethrow ids do not match";
        rethrows[id] = rt;

    }
    return rethrows;
}

function multiedges(hand, rethrow) {
    local kept = {};
    local s = 0;
    for[i in 0..4] {
        if(!rethrow[i]) {
            kept.add(hand[i]);
        } else {
            s += 1;
        }
    }
    local edges = {};
    for[i in 0..floor(pow(6, s))-1] {
        local t = {};
        for[v in kept.values()] t.add(v);
        local k = i;
        for[j in 0..s-1] {
            t.add(k%6+1);
            k = floor(k/6);
        };
        t = sorted(t);
        if (t.count() != 5) throw "multiedge error";
        local tid = handToId(t);
        if (edges[tid] is nil) {
            edges[tid] = 1;
        } else {
            edges[tid] += 1;
        }
    }
    return edges;
}

function lookup(hid, rtid) {
    if (graph[hid] is nil || graph[hid][rtid] is nil) {
        graph[hid][rtid] = multiedges(hands[hid], rethrows[rtid]);
    }
    return graph[hid][rtid];
}

function expectedScore(hand, rethrow) {
    local hid = handToId(hand);
    local rtid = rethrowToId(rethrow);
    local edges = lookup(hid, rtid);
    local nbEdges = 0;
    local score = {};
    for[h,c in edges] {
        nbEdges += c;
        local s = eval(handFromId(h));
        for[k,v in s] {
            if(score[k] is nil) {
                score[k] = c*v;
            } else {
                score[k] += c*v;
            }
        }
    }
    for[k in score.keys()] score[k] /= nbEdges;
    return score;
}

function mean(e, available_squares) {
    return sum[k in available_squares](e[k]) / available_squares.count();
}

function containsValue(m, e) {
    for[v in m.values()] if(v == e) return true;
    return false;
}

function roll_dice(hand, available_squares) {
    local bestValue = -1;
    local bestMean = -1;
    local bestRethrow = nil;
    for[rtid, rethrow in rethrows] {
        local score = expectedScore(hand, rethrow);
        local m = mean(score, available_squares);
        for[k in all_squares()] {
            if(!containsValue(available_squares, k)) continue;
            local v = score[k];
            if(v > bestValue || (v == bestValue && m > bestMean)) {
                bestValue = v;
                bestMean = m;
                bestRethrow = rtid;
            }
        }
    }
    if(bestRethrow is nil) throw "cannot return nil rethrow";
    // println("recommending rethrow ", rethrowFromId(bestRethrow), " with value ", bestValue);
    return rethrowFromId(bestRethrow);
}

function choose_decision(hand, available_squares) {
    local bestValue = -1;
    local bestSquare = nil;
    local score = eval(hand);
    for[k in available_squares] {
        local v = score[k];
        if(v > bestValue) {
            bestValue = v;
            bestSquare = k;
        }
    }
    if(bestSquare is nil) throw "cannot return nil square";
    return bestSquare;
}

function toHand(s) {
    local sd = s.split(",");
    if(sd.count() != 5) throw "hand must have 5 dice";
    local dice = {};
    for[d in sd] dice.add(d.toInt());
    return dice;
}

function main(args) {
    if(args.count() != 3) throw "must call with three argument";
    if(args[0] == "reroll") {
        local hand = toHand(args[1]);
        local available_squares = args[2].split(",");
        graph = {};
        hands = createHands();
        rethrows = createRethrows();
        reroll = roll_dice(hand, available_squares);
        // println(reroll);
    } else if(args[0] == "decision") {
        local hand = toHand(args[1]);
        local available_squares = args[2].split(",");
        decision = choose_decision(hand, available_squares);
        // println(decision);
    } else {
        throw "first argument must be \"reroll\" or \"decision\"";
    }
}