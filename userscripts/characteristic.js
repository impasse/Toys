// ==UserScript==
// @name               国服特色
// @namespace          http://github.com/impasse
// @version            0.8
// @match              https://uwuowo.mathi.moe/**/*
// @description         为 uwuowo 增加国服特色数值
// @description:zh-CN   为 uwuowo 增加国服特色数值
// @license            MIT
// @grant              none
// ==/UserScript==

(function () {
    'use strict';

    const originalFetch = window.fetch;

    const characteristic = {
        "Drizzle": 1.045,
        "Wind Fury": 1.061,
        "Grace of the Empress": 1,
        "Order of the Emperor": 1,
        "Barrage Enhancement": 1.05,
        "Firepower Enhancement": 1.03,
        "Recurrence": 1,
        "True Courage": 1,
        "Berserker Technique": 1.06,
        "Mayhem": 1.06,
        "Asura's Path": 1.03,
        "Brawl King Storm": 1.05,
        "Enhanced Weapon": 1.02,
        "Pistoleer": 1.04,
        "Remaining Energy": 1.07,
        "Surge": 1.07,
        "Gravity Training": 1.134,
        "Rage Hammer": 1.12,
        "Control": 1.123,
        "Pinnacle": 1.123,
        "Combat Readiness": 1.08,
        "Lone Knight": 1.08,
        "Peacemaker": 1.02,
        "Time to Hunt": 1.02,
        "Arthetinean Skill": 1.06,
        "Evolutionary Legacy": 1.08,
        "Judgment": 1,
        "Hunger": 1.12,
        "Lunar Voice": 1.12,
        "Shock Training": 1.1,
        "Ultimate Skill: Taijutsu": 1.1,
        "Demonic Impulse": 1.08,
        "Perfect Suppression": 1.05,
        "Death Strike": 1.06,
        "Loyal Companion": 1.06,
        "Predator": 1.03,
        "Punisher": 1.03,
        "Igniter": 1.02,
        "Reflux": 1.02,
        "Full Moon Harvester": 1.03,
        "Night's Edge": 1.03,
        "Energy Overflow": 1.077,
        "Robust Spirit": 1.077,
        "Deathblow": 1.12,
        "Esoteric Flurry": 1.06,
        "Communication Overflow": 1.053,
        "Master Summoner": 1.053,
        "Esoteric Skill Enhancement": 1,
        "First Intention": 1,
        "Ferality": 1,
        "Phantom Beast Awakening": 1
    };

    const translation = {
        "Drizzle": "绵绵细雨",
        "Wind Fury": "狂风暴雨",
        "Grace of the Empress": "王后恩赐",
        "Order of the Emperor": "国王圣谕",
        "Barrage Enhancement": "炮击强化",
        "Firepower Enhancement": "火力强化",
        "Recurrence": "归元",
        "True Courage": "勇气激发",
        "Berserker Technique": "狂战士秘技",
        "Mayhem": "疯狂",
        "Asura's Path": "修罗之路",
        "Brawl King Storm": "拳王破天舞",
        "Enhanced Weapon": "强化武器",
        "Pistoleer": "手枪手",
        "Remaining Energy": "弥留之息",
        "Surge": "爆裂",
        "Gravity Training": "重力修练",
        "Rage Hammer": "愤怒之锤",
        "Control": "节制",
        "Pinnacle": "巅峰",
        "Combat Readiness": "战斗姿态",
        "Lone Knight": "孤独的骑士",
        "Peacemaker": "和平之光",
        "Time to Hunt": "狩猎时刻",
        "Arthetinean Skill": "阿尔泰因科技",
        "Evolutionary Legacy": "超同步核心",
        "Judgment": "裁决许可",
        "Hunger": "饥渴",
        "Lunar Voice": "月声",
        "Shock Training": "冲击修炼",
        "Ultimate Skill: Taijutsu": "极义：体术",
        "Demonic Impulse": "无尽冲动",
        "Perfect Suppression": "完美抑制",
        "Death Strike": "终结袭击",
        "Loyal Companion": "第二个伙伴",
        "Predator": "捕食者",
        "Punisher": "处决者",
        "Igniter": "点火",
        "Reflux": "环流",
        "Full Moon Harvester": "满月鬼门开",
        "Night's Edge": "晦朔边界",
        "Energy Overflow": "经脉打通",
        "Robust Spirit": "逆天之体",
        "Deathblow": "一击必杀",
        "Esoteric Flurry": "奥义乱舞",
        "Communication Overflow": "心有灵犀",
        "Master Summoner": "高阶召唤",
        "Esoteric Skill Enhancement": "奥义精通",
        "First Intention": "赤子之心",
        "Ferality": "野性",
        "Phantom Beast Awakening": "幻兽觉醒"
    };


    window.fetch = function (url, ...options) {
        return originalFetch.apply(this, [url, ...options])
            .then(response => {
                const clonedResponse = response.clone();

                if (url.startsWith('/api/stats/raids?boss')) {
                    return clonedResponse.json().then(data => {
                        const newStats = data.stats.map(item => {
                            if (characteristic[item.spec]) {
                                const characteristicValue = characteristic[item.spec];
                                ['q1', 'q3', 'lowerWhisker', 'upperWhisker', 'max', 'median'].forEach(key => {
                                    item[key] = item[key] * characteristicValue;
                                });
                                if (translation[item.spec]) {
                                    item.spec = translation[item.spec];
                                }
                                item.topEncounters = item.topEncounters.map(encounter => {
                                    return {
                                        ...encounter,
                                        dps: encounter.dps * characteristicValue,
                                    };
                                });
                            }
                            return item;
                        });
                        const newResponse = new Response(JSON.stringify({ ...data, stats: newStats }), {
                            status: response.status,
                            statusText: response.statusText,
                            headers: response.headers
                        });
                        Object.defineProperty(newResponse, 'url', {
                            value: response.url
                        });
                        return newResponse;
                    });
                } else if (url.startsWith('/api/stats/raids/combat-power')) {
                    return clonedResponse.json().then(data => {
                        const newData = data.map(item => {
                            if (characteristic[item.spec]) {
                                item.avg = item.avg * characteristic[item.spec];
                            }
                            if (translation[item.spec]) {
                                item.spec = translation[item.spec];
                            }
                            return item;
                        });
                        const newResponse = new Response(JSON.stringify(newData), {
                            status: response.status,
                            statusText: response.statusText,
                            headers: response.headers
                        });
                        Object.defineProperty(newResponse, 'url', {
                            value: response.url
                        });
                        return newResponse;
                    });
                } else {
                    return response;
                }
            })
            .catch(error => {
                console.error('Fetch error:', error);
                throw error;
            });
    };
})();
